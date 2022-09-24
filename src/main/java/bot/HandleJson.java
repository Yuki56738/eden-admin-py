package bot;

import com.google.gson.Gson;
import com.google.gson.stream.JsonWriter;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

public class HandleJson {
    public static void createJsonFile(Map map, String path) throws IOException {
//        if (!Files.exists(Paths.get(path))) {
//            try {
//                Files.createFile(Paths.get(path));
//            } catch (IOException e) {
//                throw new RuntimeException(e);
//            }
//        }
        Gson gson = new Gson();
        OutputStreamWriter outputStreamWriter = new OutputStreamWriter(new FileOutputStream(path));
        JsonWriter jsonWriter = new JsonWriter(outputStreamWriter);
        gson.toJson(map, map.getClass(), jsonWriter);
    }
    public static Map readJsonFile(String path) throws FileNotFoundException {
        Gson gson = new Gson();
        InputStreamReader inputStreamReader = new InputStreamReader(new FileInputStream(path));
        Map tmpMap = gson.fromJson(inputStreamReader, Map.class);
        return tmpMap;
    }
}
