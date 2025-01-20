from django.db import models

from getmentor.utilities.db.abstract_models.basemodel import (BaseModel,
                                                              BaseModelManager)


class Seniority(BaseModel):
    industry = models.ForeignKey('mentors.Industry', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text="Name of the seniority e.g. Tech industry: "
                                                      "Entry Level"
                                                      "Intermediate"
                                                      "Senior, Manager"
                                                      "Director, Lead"
                                                      "Executive, Founder")

    class Meta:
        unique_together = ("industry", "name")

    def __str__(self):
        return f"{self.industry} ({self.name})"

    objects = BaseModelManager()
