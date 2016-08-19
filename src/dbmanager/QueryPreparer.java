package dbmanager;

/**
 * Created by Timothy on 8/18/16.
 */

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.UUID;

class QueryPreparer {
    // TODO(pallarino): Validate the inputs.

    QueryPreparer() {}

    // TODO(pallarino): Take in a JSON Object instead and don't take in a connection but initialize the class with the connection perhaps.
    boolean insertListing(Connection connection,
                          double breakPrice,
                          String description,
                          String name) {
        String sql = "INSERT INTO listing (\n" +
                "listing_id, broken_price, description, name)\n" +
                "VALUES (?, ?, ?, ?)\n";

        PreparedStatement statement = null;
        try {
            statement = connection.prepareStatement(sql);
            statement.setObject(1, UUID.randomUUID());
            statement.setDouble(2, breakPrice);
            statement.setObject(3, description);
            statement.setObject(4, name);
            int updated = statement.executeUpdate();
            return updated != 0;
        } catch (SQLException e) {
            e.printStackTrace();
            System.out.println("Invalid Prepared Statement");
            return false;
        }
    }

    boolean getListing() {
        return true;
    }
}
