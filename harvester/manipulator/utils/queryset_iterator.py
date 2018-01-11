"""
Contains the queryset_iterator function.
This function is useful for iterating over large queryset with Django.
"""
import gc


def queryset_iterator(queryset, chunksize=2000):
    """
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered
    query sets.
    """
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()


def chunk_copy(from_model, to_model, fields, chunksize=2000,
               ignore_existence=None, using='default'):
    """Chunk copy values from one model to another model

    :param ignore_existence: the fields to ignore_existence,
    For example ignore_existence=('message_id', 'pk'),
    This will use update_or_create(defaults=value, ...) to single
    create_or_update rows
    :param using: database using
    :param fields: share fields of ``from_model`` and ``to_model``
    """
    chunk = list()
    queryset = from_model.objects.using(using).all()

    for row in queryset_iterator(queryset, chunksize):
        values = {field: getattr(row, field) for field in fields}

        if ignore_existence:
            ignore_existence_values = {
                field: getattr(row, field) for field in ignore_existence
                }
            r = to_model.objects.using(using).update_or_create(
                defaults=values,
                **ignore_existence_values
            )
            print('%s => %s, %s' % (
                repr(from_model), repr(to_model), repr(r)))

        elif chunksize:
            chunk.append(to_model(**values))
            if len(chunk) == chunksize:
                to_model.objects.using(using).bulk_create(chunk)
                print('%s => %s, %d Created' % (
                    repr(from_model), repr(to_model), chunksize))
                chunk = []
