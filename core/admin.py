# core/admin.py

from django.contrib import admin

from .models import Modulo, Exercicio, Alternativa, Progresso

class AlternativaInline(admin.TabularInline):
    # - Permite cadastrar alternativas junto com o exercício, na mesma tela.

    model = Alternativa
    extra = 2

@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ("enunciado", "modulo", "tipo", "dificuldade")
    list_filter = ("modulo", "tipo", "dificuldade")
    search_fields = ("enunciado",)
    inlines = [AlternativaInline]

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ("nome", "ordem")
    ordering = ("ordem", )


@admin.register(Progresso)
class ProgressoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "modulo", "status", "pontos", "atualizado_em")
    list_filter = ("status", )