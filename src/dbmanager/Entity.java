package dbmanager;

/**
 * Created by Timothy on 8/20/16.
 */
// TODO(pallarino): Extends key type?
abstract class Entity<K>{

    abstract K getKey();
}
