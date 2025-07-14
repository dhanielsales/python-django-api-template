ISSUES
https://github.com/typeddjango/django-stubs/issues/1684#issuecomment-1706446344

# Use the default managers for the models.

# This is necessary to ensure that the repository

# can interact with the models correctly.

# Issue: https://github.com/typeddjango/django-stubs/issues/1684#issuecomment-1706446344

self.deal_manager = DealModel.\_default_manager
self.distributor_manager = DistributorModel.\_default_manager
self.tags_manager = TagModel.\_default_manager
