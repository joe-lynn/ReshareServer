package dbmanager;

/**
 * Created by Timothy on 8/14/16.
 */
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

import java.sql.Connection;
import java.sql.DriverManager;

// TODO(pallarino): Rename this class.
// TODO(pallarino): Do I need to connect to database over HTTPS?
class ConnectionManager {
    private static final String DB_PATH = "./db/config/items_config";

    void initialize() {
        Connection c = null;
        try {
            File config = new File(DB_PATH);
            BufferedReader reader = new BufferedReader(new FileReader(config));
            DatabaseCredentials credentials = new DatabaseCredentials();
            String line;
            // TODO(stfinancial): Better way to parse this in the future, use XML perhaps and wrapper class.
            credentials.dbName = reader.readLine();
            credentials.username = reader.readLine();
            credentials.password = reader.readLine();
            Class.forName("org.postgresql.Driver");
            c = DriverManager.getConnection("jdbc:postgresql://" + credentials.dbName,
                    credentials.username, credentials.password);
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println(e.getClass().getName()+": "+e.getMessage());
            System.exit(0);
        }
        System.out.println("Opened database successfully");
    }

    private class DatabaseCredentials {
        private String dbName;
        private String username;
        private String password;
    }
}