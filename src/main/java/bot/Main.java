package bot;

import io.github.cdimascio.dotenv.Dotenv;
import org.javacord.api.DiscordApi;
import org.javacord.api.DiscordApiBuilder;
import org.javacord.api.entity.channel.*;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.MessageSet;
import org.javacord.api.entity.user.User;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

import static java.lang.Boolean.FALSE;
import static java.lang.Boolean.TRUE;

public class Main {
    public static void main(String[] args) {
        String TOKEN = null;
        Dotenv dotenv = Dotenv.load();
        TOKEN = dotenv.get("DISCORD_TOKEN");
        DiscordApi api = new DiscordApiBuilder()
                .setToken(TOKEN)
                .setAllIntents()
                .login().join();
        System.out.println("bot built");

        TextChannel prof_channel = (TextChannel) api.getChannelById("995656569301774456").get();
        TextChannel prof2_channel = (TextChannel) api.getChannelById("1016234230549843979").get();
        Map<String, String> userTextChannelMap = new HashMap();
        Map<String, String> userServerVoiceChannelMap = new HashMap();
        Map<String, String> duoUserVoiceChannelMap = new HashMap();
        List<String> duoUsers = new ArrayList<>();
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


            if (event.getChannel().getIdAsString().equalsIgnoreCase("1019948085876629516")) {

                serverVoiceChannel = new ServerVoiceChannelBuilder(event.getServer())
                        .setName(String.format("%sの部屋", event.getUser().getDisplayName(event.getServer())))
                        .setUserlimit(2)
                        .setCategory(api.getChannelCategoryById("1012943676332331118").get())
                        .create().join();
                serverTextChannel = new ServerTextChannelBuilder(event.getServer())
                        .setName(event.getUser().getIdAsString())
                        .setCategory(api.getChannelCategoryById("1019540126336032819").get())
                        .create().join();
                userTextChannelMap.put(event.getUser().getIdAsString(), serverTextChannel.getIdAsString());
                userServerVoiceChannelMap.put(event.getUser().getIdAsString(), serverVoiceChannel.getIdAsString());
                event.getUser().move(serverVoiceChannel);
                for (Message x : profMessages) {
                    if (x.getAuthor().getIdAsString().equalsIgnoreCase(event.getUser().getIdAsString())) {
                        ServerTextChannel serverTextChannel1 = api.getServerTextChannelById(serverTextChannel.getIdAsString()).get();
                        serverTextChannel1.sendMessage(x.getContent());
                        break;
                    }
                }
                for (Message x : prof2Messages) {
                    if (x.getAuthor().getIdAsString().equalsIgnoreCase(event.getUser().getIdAsString())) {
                        ServerTextChannel serverTextChannel1 = api.getServerTextChannelById(serverTextChannel.getIdAsString()).get();
                        serverTextChannel1.sendMessage(x.getContent());
                        serverTextChannel1.sendMessage(event.getUser().getMentionTag());
                        serverTextChannel1.sendMessage("y.ren [名前] で部屋の名前を変える.");
                        break;
                    }
                }
            }
            for (User x : event.getChannel().getConnectedUsers()) {
                ServerTextChannel serverTextChannel1 = api.getServerTextChannelById(userTextChannelMap.get(x.getIdAsString())).get();
                ServerVoiceChannel serverVoiceChannel1 = api.getServerVoiceChannelById(userServerVoiceChannelMap.get(x.getIdAsString())).get();
                for (Message x2 : profMessages) {
                    if (x2.getAuthor().getIdAsString().equalsIgnoreCase(event.getUser().getIdAsString())) {
                        serverTextChannel1.sendMessage(x2.getContent());

                    }
                }
                for (Message x3 : prof2Messages) {
                    if (x3.getAuthor().getIdAsString().equalsIgnoreCase(event.getUser().getIdAsString())) {
                        serverTextChannel1.sendMessage(x3.getContent());
                        serverTextChannel1.sendMessage(event.getUser().getMentionTag());

                    }
                }
            }

        });
        api.addServerVoiceChannelMemberLeaveListener(event -> {
            if (userServerVoiceChannelMap.containsKey(event.getUser().getIdAsString())) {
                ServerTextChannel serverTextChannel = api.getServerTextChannelById(userTextChannelMap.get(event.getUser().getIdAsString())).get();
                ServerVoiceChannel serverVoiceChannel = api.getServerVoiceChannelById(userServerVoiceChannelMap.get(event.getUser().getIdAsString())).get();

                if (serverVoiceChannel.getConnectedUserIds().isEmpty()) {
                    serverVoiceChannel.delete();
                    serverTextChannel.delete();
                    userServerVoiceChannelMap.remove(event.getUser().getIdAsString());
                    userTextChannelMap.remove(event.getUser().getIdAsString());
                    duoUsers.remove(event.getUser().getIdAsString());
                    System.out.println("deleted.");
                }
            }
        });
        api.addMessageCreateListener(event -> {
            if (event.getMessageContent().startsWith("y.ren")) {
                ServerVoiceChannel serverVoiceChannel = api.getServerVoiceChannelById(userServerVoiceChannelMap.get(event.getMessageAuthor().getIdAsString())).get();
                serverVoiceChannel.updateName(event.getMessageContent().replaceAll("y.ren", ""));
            }
        });
    }
}
