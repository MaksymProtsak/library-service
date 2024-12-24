from django.db import models

COVER_CHOICES = [
    ("HARD", "Hard",),
    ("SOFT", "Soft",),
]


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
    inventory = models.IntegerField(default=1)

    def update_inventory(self):
        count = Book.objects.filter(title=self.title).count()
        Book.objects.filter(title=self.title).update(inventory=count)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_inventory()

    def __str__(self):
        return (
            f"{self.title} by {self.author} "
            f"({self.get_cover_display()}) - ${self.daily_fee}/day "
            f"(in stock: {self.inventory})"
        )
