package dbmanager;

import com.zaxxer.hikari.HikariConfig;

import java.io.*;

// TODO(pallarino): If we stay with Hikari, this may not be needed as HikariConfig can read file directly, the config must simply be reformatted.

/**
 * Contains configuration settings for a Database.
 */
// TODO(pallarino): This should not be public, will not be public when wrapper is created.
public class DatabaseConfig {
    private String configFilePath;
    private String dbName;
    private String password;
    private String username;

    private HikariConfig hikariConfig;

    // TODO(pallarino): Multiple exception handling is needed, one for file not found, the other for invalid config file.

    /**
     * Constructs a DatabaseConfig object from a path to a config file.
     * @param configFile - Path to the database config file.
     * @throws IOException - Throws a FileNotFoundException if the config file cannot be found, and IOException if config file cannot be read properly.
     */
    // TODO(pallarino): This should not be public!!! Get rid of this public when wrapper is written.
    public DatabaseConfig(String configFile) throws IOException {
        // TODO(pallarino): Instead of reading the file ourselves, can pass to HikariConfig and then read the properties.
        BufferedReader reader = new BufferedReader(new FileReader(new File(configFile)));
        // TODO(pallarino): A more reliable way to read config (think XML or JSON)
        dbName = reader.readLine();
        username = reader.readLine();
        password = reader.readLine();
        reader.close();

        // TODO(pallarino): Pass the file directly when we are happy with using Hikari.
        hikariConfig = new HikariConfig();
        hikariConfig.setDataSourceClassName("org.postgresql.ds.PGSimpleDataSource");
        hikariConfig.setJdbcUrl("jdbc:postgresql://" + dbName);
        hikariConfig.setUsername(username);
        hikariConfig.setPassword(password);
    }

    // TODO(pallarino): Think about these accessors and whether things should be given access to these, how to better make private.
    HikariConfig getHikariConfig() { return hikariConfig; }
    String getName() { return dbName; }
    String getPassword() { return password; }
    String getUsername() { return username; }

    @Override
    public String toString() {
        return dbName + "/" + username;
    }
}
