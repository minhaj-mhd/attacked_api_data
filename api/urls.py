
from django.urls import path
from .views import AttackList, AttackRecent, AttackStatistics, AttackVisualizationData

urlpatterns = [
    path('attacks/', AttackList.as_view(), name='attack-list'),
    path('attacks/recent/', AttackRecent.as_view(), name='attack-recent'),
    path('attacks/statistics/', AttackStatistics.as_view(), name='attack-statistics'),
    path('attacks/visualization-data/', AttackVisualizationData.as_view(), name='attack-visualization-data'),
]
