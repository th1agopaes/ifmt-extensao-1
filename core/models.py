# core/models.py

from django.db import models
from django.conf import settings

# Classe dos Módulos
class Modulo(models.Model):
    # - Representa uma área de conteúdo (ex: Operações básicas, tabuada).

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    icone = models.CharField(
        max_length=50,
        blank=True,
        help_text="Nome ou classe do ícone usado na interface."
    )
    ordem = models.PositiveIntegerField(
        default=0,
        help_text="Define a ordem de exibição dos módulos na tela inicial"
    )

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ["ordem"]

    def __str__(self):
        return self.nome

# Classe dos exercícios
class Exercicio(models.Model):
    # - Uma questão específica, vinculada a um módulo.

    class Tipo(models.TextChoices):
        NUMERICA = "NUM", "Numérica"
        MULTIPLA_ESCOLHA = "MULT", "Múltipla escolha"

    class Dificuldade(models.TextChoices):
        FACIL = "FACIL", "Fácil"
        MEDIO = "MEDIO", "Médio"
        DIFICIL = "DIFICIL", "Difícil"

    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        related_name="exercicios"
    )
    enunciado = models.TextField()
    tipo = models.CharField(max_length=4, choices=Tipo.choices)
    dificuldade = models.CharField(
        max_length=10,
        choices=Dificuldade.choices,
        default=Dificuldade.FACIL
    )
    resposta_numerica = models.FloatField(
        null=True,
        blank=True,
        help_text="Preenchido apenas quando o tipo é númerica"
    )

    class Meta:
        verbose_name = "Exercício"
        verbose_name_plural = "Exercícios"

    def __str__(self):
        return f"[{self.modulo.nome}] {self.enunciado[:50]}"

# Classe das alternativas
class Alternativa(models.Model):
    # - Opção de resposta de um exercício de múltipla escolha

    exercicio = models.ForeignKey(
        Exercicio,
        on_delete=models.CASCADE,
        related_name="alternativas"
    )
    texto = models.CharField(max_length=255)
    correta = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"

    def __str__(self):
        marcador = "✓" if self.correta else "✗"
        return f"{marcador} {self.texto}"

# Classe para o progresso do usuário
class Progresso(models.Model):
    # - Acompanha o avanço de um usuário em um módulo específico.

    class Status(models.TextChoices):
        NAO_INICIADO = "NI", "Não iniciado"
        EM_ANDAMENTO = "EA", "Em andamento"
        CONCLUIDO = "CO", "Concluído"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progressos"
    )
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        related_name="progressos"
    )
    pontos = models.PositiveIntegerField(default=0)
    exercicios_corretos = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NAO_INICIADO
    )
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Progresso"
        verbose_name_plural = "Progressos"
        unique_together = ("usuario", "modulo")

    def __str__(self):
        return f"{self.usuario} — {self.modulo.nome} ({self.get_status_display()})"