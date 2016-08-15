package dbmanager;

/**
 * Created by Timothy on 8/14/16.
 */
public class TestConnection {
    public static void main(String[] args) {
        TestConnection t = new TestConnection();
        t.runTest();
    }

    public void runTest() {
        ConnectionManager conn = new ConnectionManager();
        conn.initialize();
    }
}
