package bot;

import com.google.gson.Gson;
import org.javacord.api.DiscordApi;
import org.javacord.api.entity.channel.*;
import org.javacord.api.entity.message.Message;
import org.javacord.api.entity.message.MessageSet;
import org.javacord.api.entity.permission.Permissions;
import org.javacord.api.entity.permission.PermissionsBuilder;
import org.javacord.api.entity.permission.Role;
import org.javacord.api.entity.permission.RoleBuilder;
import org.javacord.api.entity.user.User;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class Main2 {
    public static String NEXTVC;

    public static void main(DiscordApi api) {
        TextChannel prof_channel = (TextChannel) api.getChannelById("995656569301774456").get();
        Map<String, String> userTextChannelMap = new HashMap();
        Map<String, String> userServerVoiceChannelMap = new HashMap();
        Map<ServerVoiceChannel, Role> serverVoiceChannelRoleMap = new HashMap<>();
        Map<String, List<String>> serverVoiceChannelUserListMap = new HashMap<>();
        Map<String, String> vcTxtMap = new HashMap<>();
        api.addServerVoiceChannelMemberJoinListener(event -> {
            MessageSet profMessages = null;
            ServerVoiceChannel serverVoiceChannel = null;
            ServerTextChannel serverTextChannel = null;
            try {
                profMessages = prof_channel.getMessages(1000).get();

            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } catch (ExecutionException e) {
                throw new RuntimeException(e);
            }


            if (event.getChannel().getIdAsString().equalsIgnoreCase("1022093347793408010")) {
                System.out.println(event.getUser().getDisplayName(event.getServer()));
                Permissions allDeniedPermissions = new PermissionsBuilder().setAllDenied().build();
                Permissions permissions1 = Permissions.fromBitmask(Long.valueOf("689379286592"));
                Permissions permissions2 = Permissions.fromBitmask(Long.valueOf("36701696"));
                Role everyoneRole = api.getRoleById("994483180927201400").get();
                Role memberRole = api.getRoleById("997644021067415642").get();
                Role tempRole;
                tempRole = new RoleBuilder(event.getServer())
                        .setName(event.getUser().getConnectedVoiceChannel(event.getServer()).get().getIdAsString())
                        .create().join();


                serverVoiceChannel = new ServerVoiceChannelBuilder(event.getServer())
                        .addPermissionOverwrite(everyoneRole, allDeniedPermissions)
                        .addPermissionOverwrite(memberRole, permissions2)
                        .setName(String.format("%sの部屋", event.getUser().getDisplayName(event.getServer())))
                        .setUserlimit(2)
                        .setCategory(api.getChannelCategoryById("1019608718310133780").get())
                        .create().join();
                serverTextChannel = new ServerTextChannelBuilder(event.getServer())
                        .addPermissionOverwrite(everyoneRole, allDeniedPermissions)
//                        .addPermissionOverwrite(memberRole, allDeniedPermissions)
//                        .addPermissionOverwrite(memberRole, permissions2)
                        .addPermissionOverwrite(tempRole, permissions1)
                        .setName(String.format("%sの部屋", event.getUser().getDisplayName(event.getServer())))
                        .setCategory(api.getChannelCategoryById("1019608718310133780").get())
                        .create().join();
                event.getUser().addRole(tempRole).join();
                userTextChannelMap.put(event.getUser().getIdAsString(), serverTextChannel.getIdAsString());
                userServerVoiceChannelMap.put(event.getUser().getIdAsString(), serverVoiceChannel.getIdAsString());
                serverVoiceChannelRoleMap.put(serverVoiceChannel, tempRole);
                vcTxtMap.put(serverVoiceChannel.getIdAsString(), serverTextChannel.getIdAsString());
                System.out.println("***vcTxtMap:");
                System.out.println(vcTxtMap);
                System.out.println("Created channel:");
                System.out.println(serverVoiceChannel.getName());
                System.out.println(serverTextChannel.getName());
                event.getUser().move(serverVoiceChannel);

                List<String> userList1 = new ArrayList<>();
                userList1.add(event.getUser().getIdAsString());
                serverVoiceChannelUserListMap.put(serverVoiceChannel.getIdAsString(), userList1);
                System.out.println(String.format("in first vc event: %s", serverVoiceChannelUserListMap));
                NEXTVC = serverVoiceChannel.getIdAsString();

                for (Message x : profMessages) {
                    if (x.getAuthor().getIdAsString().equalsIgnoreCase(event.getUser().getIdAsString())) {
                        ServerTextChannel serverTextChannel1 = api.getServerTextChannelById(serverTextChannel.getIdAsString()).get();
                        String msgToSend = "y.ren [名前] で部屋の名前を変える\n" +
                                "例｜y.ren 私のおうち\n" +
                                "y.lim [人数] で部屋の人数制限を変える\n" +
                                "例｜y.lim 4（半角）\n" +
                                "y.del でチャンネルを削除";
                        serverTextChannel1.sendMessage(msgToSend);
                        serverTextChannel1.sendMessage(x.getContent());

                        serverTextChannel1.sendMessage(event.getUser().getMentionTag());
                        break;
                    }
                }
                vcTxtMap.put(serverVoiceChannel.getIdAsString(), serverTextChannel.getIdAsString());
                for (User x : event.getChannel().getConnectedUsers()) {
                    List<String> userList = serverVoiceChannelUserListMap.get(event.getChannel().getIdAsString());
                    userList.add(x.getIdAsString());
                    serverVoiceChannelUserListMap.put(event.getChannel().getIdAsString(), userList);

                    ServerTextChannel serverTextChannel1 = api.getServerTextChannelById(vcTxtMap.get(x.getIdAsString())).get();
                    ServerVoiceChannel serverVoiceChannel1 = api.getServerVoiceChannelById(userServerVoiceChannelMap.get(x.getIdAsString())).get();

                    System.out.println(String.format("in for loop: %s", serverVoiceChannelUserListMap.toString()));
                    for (Message x2 : profMessages) {
                        if (x2.getAuthor().getIdAsString().equalsIgnoreCase(event.getUser().getIdAsString())) {
                            if (!userServerVoiceChannelMap.containsKey(x2.getAuthor().getIdAsString())) {
                                serverTextChannel1.sendMessage(x2.getContent());
                                serverTextChannel1.sendMessage(event.getUser().getMentionTag());
                                tempRole = api.getRoleById(serverVoiceChannelRoleMap.get(event.getChannel()).getIdAsString()).get();
                                event.getUser().addRole(tempRole).join();
                                userServerVoiceChannelMap.put(event.getUser().getIdAsString(), event.getChannel().getIdAsString());

                            }
                        }
                    }
                }

            }
        });
        api.addServerVoiceChannelMemberLeaveListener(event -> {
            List<String> userList = serverVoiceChannelUserListMap.get(event.getChannel().getIdAsString());
            System.out.println(String.format("in memberLeaveListener: userList: %s", userList));

            for (String x : userList) {
                if (x.equalsIgnoreCase(event.getUser().getIdAsString())) {
                    ServerTextChannel serverTextChannel = null;

                    try {
                        serverTextChannel = api.getServerTextChannelById(vcTxtMap.get(event.getChannel().getIdAsString())).get();
                    } catch (Exception e) {

                    }
                    System.out.println("***connected users:*** ");
                    System.out.println(event.getChannel().getConnectedUsers().stream().count());
                    if (event.getChannel().getConnectedUsers().stream().count() == 1 || event.getChannel().getConnectedUserIds().isEmpty()) {
                        System.out.println(String.format("***delete channels hit!!****"));

                        System.out.println("deleting...");
                        System.out.println(userServerVoiceChannelMap);
                        System.out.println(userTextChannelMap);
                        serverTextChannel.delete();
                        event.getChannel().delete();
                        Role tempRole = api.getRoleById(serverVoiceChannelRoleMap.get(event.getChannel()).getId()).get();
                        tempRole = api.getRoleById(serverVoiceChannelRoleMap.get(event.getChannel()).getId()).get();
                        tempRole.delete();
                        System.out.println(event.getChannel().getConnectedUsers());
                        System.out.println(serverTextChannel.getName());

                        userServerVoiceChannelMap.remove(event.getUser().getIdAsString());
                        userTextChannelMap.remove(event.getUser().getIdAsString());
//                    duoUsers.remove(event.getUser().getIdAsString());
                        serverVoiceChannelRoleMap.remove(event.getChannel());
                        serverVoiceChannelUserListMap.remove(event.getChannel().getIdAsString());
                        serverVoiceChannelUserListMap.remove(event.getChannel().getIdAsString());
                        vcTxtMap.remove(event.getChannel().getIdAsString());
                        System.out.println("deleted.");
                        break;
                    }
//                }
                }
            }
        });
        api.addMessageCreateListener(event -> {
            ServerVoiceChannel serverVoiceChannel = null;
            ServerTextChannel serverTextChannel = null;
            if (!vcTxtMap.containsValue(event.getChannel().getIdAsString())) {
                return;
            }
            serverTextChannel = api.getServerTextChannelById(vcTxtMap.get(event.getMessageAuthor().getConnectedVoiceChannel().get().getIdAsString())).get();
            serverVoiceChannel = api.getServerVoiceChannelById(getKey(vcTxtMap, event.getChannel().getIdAsString())).get();

            if (event.getMessageContent().startsWith("y.ren")) {
                serverVoiceChannel.updateName(event.getMessageContent().replaceAll("y.ren", ""));
                serverTextChannel.updateName(event.getMessageContent().replaceAll("y.ren", ""));
            } else if (event.getMessageContent().startsWith("y.del")) {
                System.out.println("deleting...");
                System.out.println(userServerVoiceChannelMap.get(event.getMessageAuthor().getIdAsString()));
                System.out.println(userTextChannelMap.get(event.getMessageAuthor().getIdAsString()));
                serverVoiceChannel.delete();
                serverTextChannel.delete();
                Role tempRole = api.getRoleById(serverVoiceChannelRoleMap.get(event.getChannel()).getId()).get();
                tempRole.delete();
                userServerVoiceChannelMap.remove(event.getMessageAuthor().getIdAsString());
                userTextChannelMap.remove(event.getMessageAuthor().getIdAsString());
                serverVoiceChannelRoleMap.remove(event.getChannel());
                System.out.println("deleted.");
                System.out.println(userServerVoiceChannelMap);
                System.out.println(userTextChannelMap);
            } else if (event.getMessageContent().startsWith("y.lim")) {
                String msg = event.getMessageContent();
                msg = msg.replaceAll("y.lim ", "");
                int newLimit = Integer.valueOf(msg);
                serverVoiceChannel.updateUserLimit(newLimit);
            }
        });
    }

    public static <K, V> K getKey(Map<K, V> map, V value) {
        for (K key : map.keySet()) {
            if (value.equals(map.get(key))) {
                return key;
            }
        }
        return null;
    }
}

