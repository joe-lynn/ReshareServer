package dbmanager;

import com.zaxxer.hikari.HikariDataSource;
import org.json.JSONObject;

import java.sql.Connection;
import java.sql.SQLException;

/**
 * Created by Timothy on 8/20/16.
 */
public class DatabaseService {
    // TODO(pallarino): Might want to make this abstract in the future.
    private DatabaseConfig config;
    private HikariDataSource dataSource;

    DatabaseService(DatabaseConfig c) {
        config = c;
        dataSource = new HikariDataSource(c.getHikariConfig());
    }

    public boolean processRequest(JSONObject request) {
        Connection c = null;
        try {
            c = dataSource.getConnection();
            request.get("command");
            return true;
        } catch (SQLException e) {
            e.printStackTrace();
            System.out.println("Unable to get connection to " + toString());
            return false;
        }
    }

    @Override
    public String toString() {
        return config.toString();
    }
}
