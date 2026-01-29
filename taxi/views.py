from django.views.generic import ListView, DetailView
from .models import Manufacturer, Car, Driver
from django.db.models import Prefetch

class ManufacturerListView(ListView):
    model = Manufacturer
    paginate_by = 5
    # Ordernar por nome por padrão
    queryset = Manufacturer.objects.all().order_by('name')

class CarListView(ListView):
    model = Car
    paginate_by = 5
    # Otimização N+1 para o campo manufacturer
    queryset = Car.objects.select_related('manufacturer').all()

class CarDetailView(DetailView):
    model = Car
    # Opcional: Se você quiser prefetch os drivers, mas o detalhe do carro
    # pode ser suficiente com o que o template driver_detail usa para carros.
    # Para o template CarDetailView, você precisa dos drivers, então prefetch_related é bom.
    # Assumindo que o relacionamento entre Car e Driver é ManyToMany (via a tabela intermediária)
    # Se for ManyToMany (Car.drivers.all()), use prefetch_related.
    # Se for ForeignKey do Car para Driver (o que é incomum para "drivers desse carro"), use select_related.
    # Vou assumir que Car.drivers é um ManyToManyField para otimizar a exibição de drivers no detalhe do carro.
    def get_queryset(self):
        return Car.objects.select_related('manufacturer').prefetch_related('drivers').all()

class DriverListView(ListView):
    model = Driver
    paginate_by = 5
    # Assumindo que a ordenação padrão é pelo campo 'username' (ou outro campo que o default use)
    # Se precisar forçar por 'username', adicione: queryset = Driver.objects.all().order_by('username')

class DriverDetailView(DetailView):
    model = Driver
    # Otimização N+1: pré-busca os carros do motorista e o fabricante de cada carro.
    # Assumindo que Driver.cars é um ManyToManyField.
    # Se for ManyToMany, 'cars' é o nome do campo no modelo Driver que se relaciona com Car.
    # Se o campo for 'car_set' (acesso reverso), a sintaxe é diferente.
    # Usando prefetch_related('cars__manufacturer') para buscar todos os carros e seus fabricantes de uma vez.
    def get_queryset(self):
        return Driver.objects.prefetch_related(
            Prefetch('cars', queryset=Car.objects.select_related('manufacturer'))
        ).all()
