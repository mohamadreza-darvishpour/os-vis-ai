// فراخوانی اسکنر برای دریافت ورودی
import java.util.Scanner;
// فراخوانی تابع لیست برای ذخیره ی متغییر ها
import java.util.List;
// فراخوانی ارایه ها برای استفاده از ترکیب ان با لیست 
import java.util.ArrayList;

// ساخت کلاس اصلی همنام با فایل
public class list_avg{

//ساخت فانکشن اصلی تابع برای اجرا ی عملیات اصلی
public static void main(String[] args){
    
    //حلقه ی وایل برای تکرار و امتحان ورودی 
    while(true){
    // هندل کردن ارور . در این قسمت کد اجرا میشود در صورت ارور وارد بخش اکسپشن میشود.
    try{
    // نمایش پیام قبل از گرفتن ورودی از کاربر.
    System.out.print( "Enter your numbers : "   );
    // ساخت متغیر برای ذخیر ورودی دریافتی از تابع نوشته شده برای دریفت استرینگ
    String num_text = return_inputted_string();
    //ساخت یک لیست پس از شکستن استرینگ به اعداد 
    String[] num_list = num_text.split(",");
    // ساخت یک لیست با نوع ایتم ها اعشاری بلند
    List<Double> mix_list = new ArrayList<>() ;
    // ایتریت کردن ایتم های درون لیست استرینگ و تبدیل نوع انها
    for (String item : num_list ){
        // تدیل نوع استرینگ به دابل یا اعشار بلند
        double changed_type = Double.parseDouble(item);
        //اضافه کردن مقدار اعشار به لیست اعشاری
        mix_list.add(changed_type);
    }
    // محاسبه ی میانگین با استفاده از تابع ساخته شده در پایین.
    double avg = return_avg_from_list(mix_list);
    //نمایش لیست اعداد
    System.out.println("List : " + mix_list);
    // نمایش میانگین
    System.out.println("Avg = " + avg);
    }// اگر خط های درون ترای اشتباه بود خط های درون کچ اجرا میشود
    catch(Exception e ){
        // نمایش پیام مناسب در صورت خطا
        System.out.println("wrong input amount. try again.");
    }
    }
}

// یک تابع برای دریافت ورودی از کاربر و ارسال به خروجی تابع 
// نوع دسترسی پویا تا نیاز به ساخت ابجکت حاضر برای استفاده نباشد. 
// نوع خروجی استرینگ
public static String return_inputted_string(){
    // ساخت یک ابجکت اسکنر
    Scanner my_scanner = new Scanner(System.in);
    // ذخیره ی لاین ورودی از کاربر 
    String text = my_scanner.nextLine();
    //ارسال مقدار به خروجی 
    return text ;
}

// ساخت تابع پویا و نوع خروجی دابل  و نوع ورودی لیست
//محاسبه ی میانگین ایتم های درون لیست
public static double return_avg_from_list(List<Double> any_list){
    // مقدار اولیه ی 0 برای جمع با مقادیر دیگر
    double sum = 0;
    // حلقه ی فور برای ایتریت بین ایتم های لیست. که از نوع دابل هستند.
    for(double item : any_list){
    // جمع مقدار سام با آیتم حاضر 
    sum = sum + item ;
}   // تقسیم بر تعداد ایتم های لیست و ارسال خروجی
    return (sum/ any_list.size()   ) ;

}

}








