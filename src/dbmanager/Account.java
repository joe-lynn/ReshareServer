package dbmanager;

/**
 * Created by Timothy on 8/21/16.
 */

import org.json.JSONObject;

import java.util.UUID;

public class Account<UUID> extends Entity<UUID> {
    private UUID key;

    Account(JSONObject json) {
        // TODO(pallarino): Implement this.
    }

    @Override
    UUID getKey() {
        return key;
    }
}
