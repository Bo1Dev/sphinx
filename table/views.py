from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from sphinxapi import SphinxClient
from .models import User
from datetime import date, datetime


def main_index(request):
    if request.GET:
        full_name = request.GET.get('name')
        dan = request.GET.get("ot")
        gacha = request.GET.get("do")
        if full_name:
            s = SphinxClient()
            s.SetServer('127.0.0.1', 9312)
            s.SetLimits(0, 1000000)
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
            s = SphinxClient()
            s.SetServer('127.0.0.1', 9312)
            print(s)
            s.SetLimits(0, 1000000)
            result = s.Query(int(dan) and int(gacha), index = 'mytest')
            print(result)
            users = []
            print(result and result['status'] == 0 and result['total'])
            if result and result['status'] == 0 and result['total']:
                matches = {row.get('id'): row.get('weight') for row in result['matches']}
                if matches:
                    users = [u for u in User.objects.filter(id__in=matches.keys()).all()]
                    users.sort(key=lambda a: matches.get(a.id, 0))
                    return render(request, 'main/index.html', context={
                            'datas': users,
                        })
                # else:
                #     print(year_ot)
                #     print(year_do)
                #     users = User.objects.filter(birthday__gte=year_do, birthday__lte = year_ot)
                #     context = {
                #         'datas': users
                #     }
                #     return render(request, 'main/index.html',
                #                   context)
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
            s = SphinxClient()
            s.SetServer('127.0.0.1', 9312)
            s.SetLimits(0, 1000000)
            s.SetFilter()
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
            s = SphinxClient()
            s.SetServer('127.0.0.1', 9312)
            s.SetLimits(0, 1000000)
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
            s = SphinxClient()
            s.SetServer('127.0.0.1', 9312)
            s.SetLimits(offset=0, limit=1000000)
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
