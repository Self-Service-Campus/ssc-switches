// custom javascript

$(document).ready(() => {
  console.log('Document Ready!');

  $('.button').on('click', function() {
    let data = {switch: $('input[name="switch"]:checked').val(), attributes: {command: $(this).val()}};
    if($('input[name="port"]').is(':checked')){
      data.attributes.port = $('input[name="port"]:checked').val();
    }
    data.attributes = JSON.stringify(data.attributes);
    $.ajax({
      url: 'http://192.168.160.241:1337/tasks/',
      data: data,
      method: 'POST',
      dataType: "json",
    })
    .done((res) => {
      getStatus(res.task_id);
    })
    .fail((err) => {
      console.log(err);
    });
  });

  function getStatus(taskID) {
    $.ajax({
      url: `/tasks/${taskID}/`,
      method: 'GET'
    })
    .done((res) => {
      const taskStatus = res.task_status;
      let result = res.task_result;
      if(result == null){
        result = 'WAITING...';
      }else {
        console.log(result);
        result = result.success;
      }
      $('#' + res.task_id).remove();
      const html = `
        <tr id="${res.task_id}">
          <td>${res.task_id}</td>
          <td>${taskStatus}</td>
          <td>${result}</td>
        </tr>`;
      $('#tasks').prepend(html);

      if (taskStatus === 'SUCCESS' || taskStatus === 'FAILURE'){
        if(result){
          let insert = '<tr id="header">';
          for(let header in res.task_result.data[0]){
            insert += '<th>' + header + '</th>';
          }
          insert += '</tr>';
          $('#header').replaceWith(insert);
          insert = '<tbody id="result">';
          for(let line in res.task_result.data){
            insert += '<tr>';
            for(let key in res.task_result.data[line]) {
              insert += '<th>' + res.task_result.data[line][key] + '</th>';
            }
            insert += '</tr>';
          }
          insert += '</tbody>';
          $('#result').replaceWith(insert);
        }
        return false;
      }
      setTimeout(function() {
        getStatus(res.task_id);
      }, 2000);
    })
    .fail((err) => {
      console.log(err);
    });
  }

  $('input[name="switch"]').change(function() {
    $('ul[class="ports"]').hide();
    document.getElementById("ports_"+ this.value).style.display = 'block';
    $('input[name="port"]').prop('checked', false);
  });

  $('#getbutton').on('click', function() {
    let data = {switches: JSON.stringify(["detiLab-b01-sw02.ua.pt"])};
    $.ajax({
      url: '/get_data/',
      data: data,
      method: 'POST',
      dataType: "json",
    })
    .done((res) => {
      getStatus(res.task_id);
    })
    .fail((err) => {
      console.log(err);
    });
  });

});
