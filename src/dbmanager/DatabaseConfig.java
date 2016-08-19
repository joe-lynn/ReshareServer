package dbmanager;

import java.io.*;

/**
 * Contains configuration settings for a Database.
 */
class DatabaseConfig {
    private String configFilePath;
    private String dbName;
    private String password;
    private String username;

    // TODO(pallarino): Multiple exception handling is needed, one for file not found, the other for invalid config file.

    /**
     * Constructs a DatabaseConfig object from a path to a config file.
     * @param configFile - Path to the database config file.
     * @throws IOException - Throws a FileNotFoundException if the config file cannot be found, and IOException if config file cannot be read properly.
     */
    DatabaseConfig(String configFile) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(new File(configFile)));
        // TODO(pallarino): A more reliable way to read config (think XML or JSON)
        dbName = reader.readLine();
        username = reader.readLine();
        password = reader.readLine();
        reader.close();
    }

    // TODO(pallarino): Think about these accessors and whether things should be given access to these, how to better make private.
    String getDbName() { return dbName; }
    String getPassword() { return password; }
    String getUsername() { return username; }
}
