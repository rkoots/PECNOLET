from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from django.views.generic import View, TemplateView
from inventory.models import Customer, Stock , OutStock
from django.db.models import Count, Sum, Q
import json

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

class HomeView(View):
    template_name = "home.html"
    def get(self, request):
        if not self.request.user.is_authenticated:
            return render(request, "index.html")

        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        recent_stocks = Stock.objects.order_by('-id')[:10]
        recent_out_stocks = OutStock.objects.order_by('-id')[:10]
        total_stock = Stock.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        total_outstock = OutStock.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']

        stock_data = Stock.objects.all()
        outstock_data = OutStock.objects.values('stock').annotate(total_outstock=Sum('quantity'))
        stock_labels = []
        stock_quantities = []
        outstock_series = []
        for stock in stock_data:
            stock_labels.append(stock.name)
            stock_quantities.append(stock.quantity)
        for stock in stock_data:
            outstock_quantity = next((item['total_outstock'] for item in outstock_data if item['stock'] == stock.id), 0)
            outstock_series.append(outstock_quantity)


        context = {'recent_stocks': recent_stocks,
                   'recent_out_stocks':recent_out_stocks,
                   'total_stock':total_stock,
                   'total_outstock':total_outstock,
                   'original_stock':total_outstock+total_stock,
                   'stock_labels': json.dumps(stock_labels),
                   'stock_quantities': json.dumps(stock_quantities),
                   'outstock_series': json.dumps(outstock_series),
                   }
        return render(request, self.template_name, context)
