package bot;

import org.javacord.api.DiscordApi;
import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.entity.channel.*;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.MessageSet;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class Main {
    public static void main(String[] args) {
        String TOKEN = "MTAxODcyMzAzOTYyMzUyNDM1Mw.GJL0GN.HPl23v8EFJFWwBxNRpLrQzYo0caCVTrFFqhrUg";
        DiscordApi api = new DiscordApiBuilder()
                .setToken(TOKEN)
                .setAllIntents()
                .login().join();
        System.out.println("bot built");

        TextChannel prof_channel = (TextChannel) api.getChannelById("995656569301774456").get();
        TextChannel prof2_channel = (TextChannel) api.getChannelById("1016234230549843979").get();
        Map<String, String> userTextChannelMap = new HashMap();
        Map<String, String> userServerVoiceChannelMap = new HashMap();
        api.addServerVoiceChannelMemberJoinListener(event -> {
            MessageSet profMessages = null;
            MessageSet prof2Messages = null;
            ServerVoiceChannel serverVoiceChannel = null;
            ServerTextChannel serverTextChannel = null;
            try {
                profMessages = prof_channel.getMessages(1000).get();
                prof2Messages = prof2_channel.getMessages(1000).get();

            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } catch (ExecutionException e) {
                throw new RuntimeException(e);
            }
            if (event.getChannel().getIdAsString().equalsIgnoreCase("1019540030286471200")) {

                serverVoiceChannel = new ServerVoiceChannelBuilder(event.getServer())
                        .setName(String.format("%sの部屋", event.getUser().getDisplayName(event.getServer())))
                        .setUserlimit(2)
                        .setCategory(api.getChannelCategoryById("1012943676332331118").get())
                        .create().join();
                serverTextChannel = new ServerTextChannelBuilder(event.getServer())
                        .setName(event.getUser().getIdAsString())
                        .setCategory(api.getChannelCategoryById("1019540126336032819").get())
                        .create().join();
                //               userTextChannelMap.put(serverVoiceChannel.getIdAsString(), serverTextChannel.getIdAsString());
//               userServerVoiceChannelMap.put(serverTextChannel.getIdAsString(), serverVoiceChannel.getIdAsString());
                userTextChannelMap.put(event.getUser().getIdAsString(), serverTextChannel.getIdAsString());
                userServerVoiceChannelMap.put(event.getUser().getIdAsString(), serverVoiceChannel.getIdAsString());
                event.getUser().move(serverVoiceChannel);
            }
        });
        api.addServerVoiceChannelMemberLeaveListener(event -> {
//            if (userServerVoiceChannelMap.containsKey(event.getUser().getIdAsString())){
//                return;
//            }
            if (userServerVoiceChannelMap.containsKey(event.getUser().getIdAsString())) {
                ServerTextChannel serverTextChannel = api.getServerTextChannelById(userTextChannelMap.get(event.getUser().getIdAsString())).get();
                ServerVoiceChannel serverVoiceChannel = api.getServerVoiceChannelById(userServerVoiceChannelMap.get(event.getUser().getIdAsString())).get();
                if (serverVoiceChannel.getConnectedUserIds().isEmpty()) {
//                if (event.getChannel().equals(serverVoiceChannel)){
                    serverVoiceChannel.delete();
                    serverTextChannel.delete();
                    userServerVoiceChannelMap.remove(event.getUser().getIdAsString());
                    userTextChannelMap.remove(event.getUser().getIdAsString());
                    System.out.println("deleted.");
//                }
                }
            }
        });
    }
}
