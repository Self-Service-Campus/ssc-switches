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
      url: '/tasks/',
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
      if (res.task_status === 'SUCCESS' || res.task_status === 'FAILURE'){
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

});
