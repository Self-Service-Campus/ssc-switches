from django.contrib.postgres.fields import ArrayField

class Switch(models.Model):
    ip = models.CharField(primary_key=True, max_length=100, unique=True)
    hostname = models.CharField(max_length=100)
    hardware = ArrayField(models.TextField(blank=False), blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"Switch {self.id_switch}, model: {self.model_switch}, dep: {self.department}"


class Port(models.Model):
    interface = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    duplex = models.CharField(max_length=100)
    link_status = models.CharField(max_length=100)
    protocol_status = models.CharField(max_length=100)
    speed = models.CharField(max_length=100)
    access_vlan = models.CharField(max_length=100)
    native_vlan = models.CharField(max_length=100)
    trunking_vlans = ArrayField(models.TextField(blank=False), blank=False)
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE) # on_delete?

    class Meta:
        unique_together = (("interface", "switch"),)