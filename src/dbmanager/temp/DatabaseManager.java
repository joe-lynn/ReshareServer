package dbmanager.temp;

import dbmanager.DatabaseConfig;
import org.json.JSONObject;

import java.io.FileNotFoundException;
import java.io.IOException;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Created by Timothy on 8/14/16.
 */

// TODO(pallarino): Rename this class.
public class DatabaseManager {
    private static final String DATABASE_CONFIG_PATH = "./db/config/items_config";

    private Connection connection;

    // TODO(pallarino): Should this load the config or should the config be passed to it. How do we handle different database types?
    // This could potentially take a parameter at some point in the future, we will see how it plays out.
    public boolean initialize() {
        try {
            DatabaseConfig config = new DatabaseConfig(DATABASE_CONFIG_PATH);
            try {
                connection = DriverManager.getConnection("jdbc:postgresql://" + config.getDbName(), config.getUsername(), config.getPassword());
                return true;
            } catch (SQLException e) {
                e.printStackTrace();
                System.out.println("Could not connect to DB: " + config.getDbName() + " with username " + config.getUsername());
                return false;
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            System.out.println("Database config file not found at path: " + System.getProperty("user.dir") + DATABASE_CONFIG_PATH);
            return false;
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("Could not parse database config file at path: " + System.getProperty("user.dir") + DATABASE_CONFIG_PATH);
            return false;
        }

    }

    JSONObject processRequest(JSONObject request) {
        return null;
    }
}
