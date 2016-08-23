package dbmanager;

import org.json.JSONObject;

/**
 * Created by Timothy on 8/22/16.
 */
public class Listing<UUID> extends Entity<UUID> {
    private UUID listingId;
    private double brokenPrice;
    private String description;
    // private Object timestamp;
    private String name;

    Listing() {}

    Listing(JSONObject json) {

    }

    @Override
    UUID getKey() {
        return null;
    }
}
