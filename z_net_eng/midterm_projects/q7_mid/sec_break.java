// اسکنر برای دریافت ورودی
import java.util.Scanner;

//کلاس اصلی همنام با فایل
public class sec_break{

//تابع اصلی کلاس اصلی با دسترسی استاتیک و خروجی نا مشخص
public static void main(String[] args){

//حلقه ی وایل بی نهایت برای امتحان خروجی های متفاوت
while(true){
//دستور ترای برای جلوگیری از ارور 
try{
//فراخوانی تابع برنامه ریزی شده برای دریافت تبدیل و نمایش خروجی 
get_break_sec();
//دریافت ارور و در صورت ارور نمایش پیغام مناسب
}catch(Exception e){
System.out.println( "wrong input amount. try again." );
}
}

}

// تابع گرفتن تعداد ثانیه از کاربر و محاسبه ی ثانیه روز ساعت دقیقه
public static void get_break_sec(){
// پیام قبل از گرفتن ورودی
System.out.print("Input : ");
// گرفتن ورودی با تابع نوشته شده در پایین 
Long seconds = return_s_inputted();
// دریافت ثانیه برابر با باقیمانده کل بر 60 است
Long sec = seconds % 60 ; 
// هر ساعت 3600 ثانیه است پس باقیمانده بر 3600 برابر دقایق و ثانیه است
// عدد باقیمانده تقسیم بر 60 برابر با دقیقه است اما اعشاری است اگر ثانیه باقیمانده باشد پس با تبدیل به لانگ به دقیقه تبدیل میشود
Long min = (Long)((seconds%3600)/60);
// مثل محاسبه ی دقیقه باز باقیمانده هر 86400 ثانیه که یک روز است بر 3600 برابر ساعت و اعشاری است 
// با تبدیل به لانگ برابر با ساعت میشود.
Long hours = (Long)((seconds%86400)/3600);
// تبدیل تقسیم کل بر تعداد ثانیه های یک روز که 86400 است
Long days = (Long)(seconds/86400);
//نمایش پیغام مناسب
System.out.println(seconds + " is equal to: " + days + " days and " + hours + " hours and " +min+ " minutes and " + sec + "seconds.");
}

// تابع برای دریافت یک ورودی لانگ یا اینتجر بزرگ
public static long return_s_inputted(){
//ساخت شی اسکنر به همراه ورودی به کانستراکتور توسط سیستم این    
Scanner my_scanner = new Scanner(System.in) ;
//دریافت ورودی از کاربر    
long s = my_scanner.nextLong();
// ارسال به خروجی فانکشن
return s ;
}




}