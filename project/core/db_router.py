class VPNRouter:
    """
    A router to control all database operations for VPN-related models.
    """
    VPN_MODELS = {'provider', 'server', 'country', 'city', 'inip', 'outip'}

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.VPN_MODELS:
            return 'data_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.model_name in self.VPN_MODELS:
            return 'data_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {self.db_for_read(obj1), self.db_for_read(obj2)}
        return len(db_set) == 1

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'data_db':
            return model_name in self.VPN_MODELS
        if db == 'default':
            return model_name not in self.VPN_MODELS
        return False
