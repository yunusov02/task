import uuid
from django.db import models
from django.utils import timezone




class SoftDeleteQuerySet(models.query.QuerySet):
    
    def delete(self):
        self.update(deleted_at=timezone.now())
        
    def restore(self):
        self.update(deleted_at=None)
        
    def hard_delete(self):
        super().delete()
        
    def alive(self):
        return self.filter(deleted_at__isnull=True)
    
    def dead(self):
        return self.filter(deleted_at__isnull=False)
    


class SoftdeleteManager(models.Manager):
    
    def get_queryset(self):
        return SoftDeleteQuerySet(
            self.model,
            using=self._db,
        ).alive()
        
        
class AllObjectsManager(models.Manager):
    
    def get_queryset(self):
        return SoftDeleteQuerySet(
            self.model,
            using=self._db
        )
        
        
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftdeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True
        
        
    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    def hard_delete(self):
        super().delete()
        
        
