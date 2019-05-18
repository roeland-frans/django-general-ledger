class PermittedMixin(object):
    """
    Adds a for_user method to applied models returning a queryset containing
    only those objects the provided user should have access to.
    """

    @classmethod
    def for_user(cls, user):
        return cls.permitted_filter(queryset=cls.objects, user=user)

    @classmethod
    def permitted_filter(cls, queryset, user):
        """
        Restricts queryset to only those objects that should be accessible
        by the provided user.

        @param queryset Queryset: queryset to be filtered.
        @param user User: user object for which to filter queryset.
        @return QuerySet: filtered to contain only those objects that should be
            accessible by the provided user.
        """
        raise NotImplementedError(
            "%s does not have an permitted_filter method implementation(required by PermittedMixin.for_user)."
            % cls
        )
