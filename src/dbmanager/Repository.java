package dbmanager;

import java.util.UUID;
import java.util.function.Function;

/**
 * Created by Timothy on 8/20/16.
 */
interface Repository<T extends Entity> {
    void delete(T entity);
    void insert(T entity);
    void update(T entity);
    void find(Function<T, T> constraint);
}
