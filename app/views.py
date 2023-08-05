import logging

from app.draw import calc_wheel_rotations, get_prize_result, set_code_used, get_prize
from app.forms import DrawForm
from app.models import Draw, Prize, UniqueCode
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


# Get an instance of a logger
logger = logging.getLogger(__name__)


# @csrf_exempt
def draw_spin(request):
    logger.info(f"Draw_new with {request.method}")
    prizes = get_list_or_404(Prize)

    if request.method == "POST":
        form = DrawForm(request.POST)
        if form.is_valid():  # and code is valid (checked on form class)
            # email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            # logger.info(f"email [{email}] code [{code}]")

            instance = form.save(commit=False)
            instance.date = timezone.now()

            try:
                ucode = UniqueCode.objects.get(code=code)
            except (Exception,) as e:
                ucode = UniqueCode(code='NO CODE', used=False, prize=None)

            if ucode.prize:
                instance.rotation = calc_wheel_rotations(ucode.prize.id)
                instance.prize = ucode.prize
            else:
                instance.rotation = calc_wheel_rotations()
                instance.prize = get_prize(get_prize_result(instance.rotation))
            instance.save()

            set_code_used(code, True)

            return render(request, 'index.html',
                          {'form': form, 'spin': True, 'result': instance.pk, 'rotation': instance.rotation, 'prizes': prizes})
        else:  # invalid form
            logger.warning(f"invalid form else => {form.is_valid()} {form.errors}")
            form = DrawForm(request.POST)
    else:
        form = DrawForm()  # No post data

    return render(request, 'index.html',
                  {'form': form, 'prizes': prizes})


def draw_result(request, pk):
    prizes = get_list_or_404(Prize)
    draw = get_object_or_404(Draw, pk=pk)
    logger.info(f"Draw with {request.method} for id {draw.pk}")
    prize = get_prize(draw.prize.pk)
    logger.info(f"Prize {prize.pk}, {prize.label}, {prize.winner}")
    if prize.try_again:
        set_code_used(draw.code, False)
    return render(request, 'draw.html', {'prizes': prizes, 'result_draw': draw, 'result_prize': prize})


def index(request):
    form = DrawForm()
    prizes = get_list_or_404(Prize)
    return render(request, 'index.html',
                  {'form': form, 'prizes': prizes})
