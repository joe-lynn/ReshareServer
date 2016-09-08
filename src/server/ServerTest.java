package server;

/**
 * Created by Timothy on 8/24/16.
 */
public class ServerTest {
    public static void main(String[] args) {
        try {
            new DiscardServer(8080).run();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
