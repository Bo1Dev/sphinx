from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from sphinxapi import SphinxClient
from .models import User
from datetime import date, datetime

def get_spx_results():
    spx = SphinxClient()
    spx.SetServer("localhost", 9312)
    spx.SetLimits(0, 1000, 1000)
    return spx

def main_index(request):
    if request.GET:
        full_name = request.GET.get('name')
        dan = request.GET.get("ot")
        gacha = request.GET.get("do")
        if full_name:
            s = get_spx_results()
            result = s.Query(full_name, index='mytest')
            users = []
            if result and result['status'] == 0 and result['total']:
                matches = {row.get('id'): row.get('weight') for row in result['matches']}
                if matches:
                    users = [u for u in User.objects.filter(id__in=matches.keys()).all()]
                    users.sort(key=lambda a: matches.get(a.id, 0))
            return render(request, 'main/index.html', {
                    'name': full_name,
                    'datas': users,
                })
        elif dan and gacha:
            s = get_spx_results()
            dan = int(dan)
            gacha = int(gacha)
            s.SetFilterRange('birthday_s', dan, gacha)
            result = s.Query("",index = 'mytest')
            users = []
            if result and result['status'] == 0 and result['total']:
                matches = {row.get('id'): row.get('weight') for row in result['matches']}
                if matches:
                    users = [u for u in User.objects.filter(id__in=matches.keys()).all()]
                    return render(request, 'main/index.html', context={
                            'datas': users,
                        })
        else:
            users = User.objects.filter(birthday__day=date.today().day, birthday__month=date.today().month)
            context = {
                'datas': users
            }
            return render(request, 'main/index.html',
                context)
    else:
        users = User.objects.filter(birthday__day=date.today().day, birthday__month=date.today().month)
        context = {
            'datas': users
        }
        return render(request, 'main/index.html',
            context)


def main_index1(request):
    if request.GET:
        last_name = request.GET.get('Last_name')
        first_name = request.GET.get('First_name')
        print(request)
        if first_name and last_name:
            s = get_spx_results()
            result = s.Query(first_name and last_name, index='mytest')
            users = []
            if result and result['status'] == 0 and result['total']:
                matches = {row.get('id'): row.get('weight') for row in result['matches']}
                if matches:
                    users = [u for u in User.objects.filter(id__in=matches.keys()).filter(
                        Q(first_name__icontains=first_name) & Q(last_name__icontains=last_name))]
                    users.sort(key=lambda a: matches.get(a.id, 0))

            return render(request, 'main/index.html',
                {
                    'first_name': first_name,
                    'datas': users,
                })
        elif first_name:
            s = get_spx_results()
            result = s.Query(first_name, index='mytest')
            users = []
            if result and result['status'] == 0 and result['total']:
                matches = {row.get('id'): row.get('weight') for row in result['matches']}
                if matches:
                    users = [u for u in
                             User.objects.filter(id__in=matches.keys()).filter(first_name__icontains=first_name)]
                    users.sort(key=lambda a: matches.get(a.id, 0))

            return render(request, 'main/index.html',
                {
                    'first_name': first_name,
                    'datas': users,
                })
        elif last_name:
            s = get_spx_results()
            result = s.Query(last_name, index='mytest')
            users = []
            if result and result['status'] == 0 and result['total']:
                matches = {row.get('id'): row.get('weight') for row in result['matches']}
                if matches:
                    users = [u for u in
                             User.objects.filter(id__in=matches.keys()).filter(last_name__icontains=last_name)]
                    users.sort(key=lambda a: matches.get(a.id, 0))

            return render(request, 'main/index.html',
                {
                    'Last_name': last_name,
                    'datas': users,
                })
        else:
            users = User.objects.filter(birthday__day=date.today().day, birthday__month=date.today().month)
            context = {
                'datas': users
            }
            return render(request, 'main/index.html',
                context)
    else:
        users = User.objects.filter(birthday__day=date.today().day, birthday__month=date.today().month)
        context = {
            'datas': users
        }
        return render(request, 'main/index.html',
            context)
