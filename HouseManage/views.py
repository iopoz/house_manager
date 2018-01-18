import datetime
import reportlab
import sys

from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, RequestContext
from reportlab.pdfbase import ttfonts, pdfmetrics
from reportlab.pdfgen import canvas

from HouseManage.forms import DateForm
from HouseManage.models import MoneyReport


def balance_data(request):
    balance_pos = MoneyReport.objects.filter(type_service=1).aggregate(Sum('money'))
    balance_neg = MoneyReport.objects.filter(type_service=2).aggregate(Sum('money'))
    if balance_pos['money__sum'] is None:
        balance_pos['money__sum'] = 0
    elif balance_neg['money__sum'] is None:
        balance_neg['money__sum'] = 0
    balance = balance_pos['money__sum'] - balance_neg['money__sum']
    now = datetime.datetime.now()
    return {'date': now.strftime("%Y-%m-%d"), 'money': balance}


def index(request):
    data = balance_data(request)
    date_form = DateForm(request.POST)
    context = {
        'balance': data['money'],
        'date': data['date'],
        'form': date_form
    }
    return render(request, 'index.html', context)


def generate_report(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    form = DateForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        start = data['before']
        end = data['after']
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="money_report_%s_%s.pdf"' % (start, end)

        # Create the PDF object, using the response object as its "file."
        MyFontObject = ttfonts.TTFont('Arial', sys.path[0] + '/HouseManage/static/Fonts/arial.ttf')
        pdfmetrics.registerFont(MyFontObject)
        p = canvas.Canvas(response)
        p.setLineWidth(.3)
        p.setFont('Arial', 12)

        db_data = MoneyReport.objects.filter(plan_date__range=(start, end))

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.

        def draw_header():
            p.setFont('Arial', 8)
            p.drawString(30, 810, "* квартира 0 - это статья расходов общедомовых нужд и приход средств от провайдеров интернета")
            p.setFont('Arial', 12)
            p.drawString(200, 770, "Отчет за период %s" % '-'.join([start, end]))
            p.drawString(30, 730, "Описание")
            p.drawString(360, 730, "Кв.")
            p.drawString(410, 730, "Сумма")
            p.drawString(470, 730, "Дата")

        def draw_body(x, y, item):
            p.drawString(x, y, item.name_service)
            p.drawString(x + 330, y, item.user.flat_number)
            p.drawString(x + 380, y, str(item.money))
            p.drawString(x + 440, y, str(item.current_date))
            if item.type_service.category_name == 'Приход':
                return {'deb': item.money, 'cred': 0}
            else:
                return {'cred': item.money, 'deb': 0}

        def draw_end(y, deb, cred, request):
            data = balance_data(request)
            p.drawString(360, y - 40, ' '.join(['Всего получено:',
                                                    str(deb)]))
            p.drawString(360, y - 60, ' '.join(['Всего потрачено:',
                                                    str(cred)]))
            p.drawString(360, y - 80, ' '.join(['Баланс на %s:' % data['date'], str(data['money'])]))

        draw_header()
        x = 30
        y = 700
        deb = 0
        cred = 0
        if len(db_data) > 0:
            for item in db_data:
                if y > 30:
                    res = draw_body(x, y, item)
                    deb += res['deb']
                    cred += res['cred']
                    y -= 20
                    x = 30
                else:
                    p.showPage()
                    y = 700
                    draw_header()
                    res = draw_body(x, y, item)
                    deb += res['deb']
                    cred += res['cred']
        draw_end(y, deb, cred, request)
        p.showPage()
        p.save()
        context = {'response': response}
        return response
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
