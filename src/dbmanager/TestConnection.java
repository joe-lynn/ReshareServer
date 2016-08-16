package dbmanager;

import java.io.File;
/**
 * Created by Timothy on 8/14/16.
 */
public class TestConnection {
    public static void main(String[] args) {
        TestConnection t = new TestConnection();
//        try {
//            String f = new File("").getCanonicalPath();
//            System.out.println(f);
//        } catch (Exception e) {
//            e.printStackTrace();
//        }

        t.runTest();
    }

    public void runTest() {
        ConnectionManager conn = new ConnectionManager();
        conn.initialize();
    }
}
