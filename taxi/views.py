from django.views.generic import ListView, DetailView
from .models import Manufacturer, Car, Driver
from django.db.models import Prefetch


class ManufacturerListView(ListView):
    model = Manufacturer
    paginate_by = 5
    queryset = Manufacturer.objects.all().order_by("name")


class CarListView(ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer").all()


class CarDetailView(DetailView):
    model = Car

    def get_queryset(self):
        # Quebra para respeitar E501
        return Car.objects.select_related("manufacturer").prefetch_related(
            "drivers"
        ).all() # Esta linha (que começa em 8 colunas de indentação) deve estar ok agora.


class DriverListView(ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(DetailView):
    model = Driver

    def get_queryset(self):
        # Otimização N+1: prefetch_related com select_related aninhado
        return Driver.objects.prefetch_related(
            Prefetch("cars", queryset=Car.objects.select_related("manufacturer"))
        ).all()
