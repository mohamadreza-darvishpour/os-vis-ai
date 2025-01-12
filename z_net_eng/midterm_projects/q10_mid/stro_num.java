//ابزار ورودی خروجی
import java.util.*;

//کلاس اصلی
public class stro_num {
    //تابع برای پیدا کردن اعداد مذکور
    // خروجی از نوع لیست
    public static List<String> findStrobogrammatic(int n) {
        return helper(n, n);
    }



public static void main(String[] args) {
// ساخت شی اسکنر
Scanner my_scanner = new Scanner(System.in);
// حلقه ی بی نهایت
while(true){
//ارور هندلینگ
try{

System.out.print("\nGiven n = ");
//دریافت ورودی
int n = my_scanner.nextInt();

System.out.print("return : " + findStrobogrammatic(n));


//ارسال پیام مناسب در صورت ارور
}catch(Exception e){
System.out.println("wrong input amount . try again.");
}


}


}

//تابع هلپر برای ساخت رشته
private static List<String> helper(int n, int originalLength) {
        // اگر 0 بود تعداد
        if (n == 0) return Arrays.asList("");
        // اگر یک باشد فقط تک رقمی ها
        if (n == 1) return Arrays.asList("0", "1", "8");

        //محاسبه کردن لیست بدون دو حالت بالا
        List<String> previousList = helper(n - 2, originalLength);
        List<String> result = new ArrayList<>();
        // لیست قبلی لیست ساخته شده ی اعداد استر است
        for (String s : previousList) {
            // برای جلوگیری از اعداد با صفر در ابتدای عدد
            if (n != originalLength) {
                result.add("0" + s + "0");
            }
            //اعداد  استرو به اول و آخر لیست قبلی  اضاف میشود
            result.add("1" + s + "1");
            result.add("6" + s + "9");
            result.add("8" + s + "8");
            result.add("9" + s + "6");
        }

        return result;
    }


}
