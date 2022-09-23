package bot;

import com.google.gson.Gson;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;

public class HandleJson {
    public static void createJsonFile(HashMap map, String path) throws FileNotFoundException {
        if (!Files.exists(Paths.get(path))) {
            try {
                Files.createFile(Paths.get(path));
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        Gson gson = new Gson();
        OutputStreamWriter outputStreamWriter = new OutputStreamWriter(new FileOutputStream(path));
        gson.toJson(map, outputStreamWriter);
    }
}
