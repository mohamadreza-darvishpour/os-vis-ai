//استفاده برای عملیات ورودی و خروج  خواندن و نوشتن
import java.io.*;
//کلاس های شبکه مثل سوکت و سرورسوکت
import java.net.*;
//ابزار لیست و اری لیست برای ذخیره متغیر ها 
import java.util.*;


//تعریف کلاس اصلی همنام با فایل 
public class mul_cli_server {
    //تعیین تعداد کاربر و پورت مشخص شده
    private static final int PORT = 12001; 
    private static final int CLIENT_COUNT = 3;

    // تابع اصلی کلاس اصلی
    public static void main(String[] args) {
        //لیست کلاینت های متصل از نوع شی سوکت
        List<Socket> clients = new ArrayList<>();
        //ساخت یک سرور که روی پورت مشخص شده گوش بدهد
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Server is listening on port " + PORT);
            //حلقه ی وایل برای تکرار پیام 
            // هر 3 پیام دریافت شده با هم ارسال میشود.
            while(true){
            //ساخت لیست پیام ها
            List<String> messages = new ArrayList<>();
            // اگر کلاینت ها کمتر از مقدار تعیین شده باشند ادامه می یابد
            while (clients.size() < CLIENT_COUNT) {
                //منتظر اتصال میماند و آن را تایید میکند.
                Socket clientSocket = serverSocket.accept();
                //کلاینت متصل شده به لیست کلاینت ها اضافه میشود.
                clients.add(clientSocket);
                
                System.out.println("Client connected: " + clients.size() + " of " + CLIENT_COUNT);
            }

            System.out.println("All clients connected. Waiting for messages...");

            //ایتریت تمام کلاینت ها 
            for (Socket client : clients) {
                // خواندن پیام ها ی متنی ارسالی از کلاینت
                BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
                //اضافه کردن پیام خوانده شده به لیست پیام ها 
                messages.add(in.readLine());
            }

            System.out.println("Messages received. Broadcasting to all clients...");

            // ایتریت کلاینت ها برای ارسال پیام
            for (Socket client : clients) {
                //ایجاد استریم خروجی برای ارسال داده به کلاینت
                PrintWriter out = new PrintWriter(client.getOutputStream(), true);
                for (String message : messages) {
                    // ارسال پیام به کلاینت
                    out.println(message.toUpperCase()); 
                }
            }

            System.out.println("Messages sent to all clients.");
        }
        } catch (Exception e) {
            e.printStackTrace(); 
        }
    }
}
