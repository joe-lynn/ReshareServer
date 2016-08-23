package dbmanager;

import com.zaxxer.hikari.HikariDataSource;
import org.json.JSONObject;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.function.Function;

/**
 * Created by Timothy on 8/20/16.
 */
public class DatabaseService {
    // TODO(pallarino): Might want to make this abstract in the future.
    private DatabaseConfig config;
    // TODO(pallarino): Make a wrapper for this in case we change underlying library.
    private HikariDataSource dataSource;

    private ListingRepository listingRepository;

    DatabaseService(DatabaseConfig c) {
        config = c;
        dataSource = new HikariDataSource(c.getHikariConfig());
        listingRepository = new ListingRepository(dataSource);
    }

    public boolean processRequest(JSONObject request) {
        Connection c = null;
        try {
            c = dataSource.getConnection();
            String command = (String) request.get("command");
            // TODO(pallarino): Better way to handle requests later, this is a hack for now.
            if (command.equals("getListings")) {

            } else {
                return false;
            }
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
