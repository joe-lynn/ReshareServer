package dbmanager;

import com.zaxxer.hikari.*;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedList;
import java.util.UUID;
import java.util.function.Function;
import java.util.List;

/**
 * Created by Timothy on 8/22/16.
 */
final class ListingRepository implements Repository<Listing> {
    private HikariDataSource dataSource;

    ListingRepository(HikariDataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public void delete(Listing entity) {

    }

    @Override
    public void insert(Listing entity) {

    }

    @Override
    public void update(Listing entity) {

    }

    @Override
    public void find(Function<Listing, Listing> constraint) {

    }

    public List<Listing> getNumListings(int number) {
//        String sql = "INSERT INTO listing (\n" +
//                "listing_id, broken_price, description, name)\n" +
//                "VALUES (?, ?, ?, ?)\n";
        String sql = "SELECT * FROM listing LIMIT ?";

        PreparedStatement statement = null;
        try {
            Connection connection = dataSource.getConnection();
            statement = connection.prepareStatement(sql);
            statement.setInt(1, number);
            ResultSet result = statement.executeQuery();
            List<Listing> listings = new ArrayList<Listing>(number);
            while (result.next()) {
                listings.add(new Listing());
            }
            connection.close();
            result.close();
            return listings;
        } catch (SQLException e) {
            e.printStackTrace();
            System.out.println("Invalid Prepared Statement");
            return Collections.emptyList();
        }
    }
}
