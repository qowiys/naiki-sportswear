from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'aplikasi' : 'Naiki Sportswear',
        'nama': 'Muhammad Qowiy Shabir',
        'class': 'PBP E'
    }

    return render(request, "main.html", context)