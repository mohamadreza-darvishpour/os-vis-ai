
// فراخوانی اسکنر برای دریافت ورودی
import java.util.Scanner; 


// کلاس اصلی همنام با فایل 
public class dig_repeat{
//تابع اصلی کلاس اصلی که اجرا میشود با دسترسی پویا و خروجی نامعلوم.
public static void main(String[] args){
// حلقه ی وایل بینهایت برای امتحان ورودی های بیشتر
while(true){
// شروع ترای ااگر اروری در دستورات داخلی باشد اکسپت اجرا میشود.
try{
//نمایش پیام مناسب به کاربر برای دریافت عدد 
System.out.print("Enter value of n : ");
//ساخت متغیر عدد لانگ برای ثبت اعداد بزرگ دریافتی از تابع دریافت کننده 
long n = return_n_inputted();
// شرط تعیین کننده ی مثبت بودن عدد 
if(n<0){
// در صورت درست بودن شرط از یک ایتریت حلقه خارج شده و دستورات بعدی را اجرا نمیکند.
System.out.println("not positive amount.");
// اجرا نشدن باقی دستورات ایتریت حاضر.
continue;}
//if n not positive or zero error
// تبدیل لانگ به استرینگ
String first = String.valueOf(n);
//تکرار کردن استرینگ عدد مربوطه.
String second = first.repeat(2) ;
String third = first.repeat(3); 
// جمع اعداد تکرار شده به همراه تبدیل همزمان انها
long sum = (n +
        Long.parseLong(second)    +
        Long.parseLong(third)
 );
//نمایش پیام مناسب به کاربر که شامل نتیجه است
System.out.println("Result("+ first +"+"+ second +"+" + third + ") : " + sum);

// در صورت ارور درستورات درون کچ اجرا و پیغام مناسب نمایش داده میشود.
}catch(Exception e){
System.out.println("wrong or huge input amount.");
}
}
}

// تعریف فانکشن با دسترسی پویا تا در کلاس حاضر نیاز به ساخت شی نباشد.
//نوع خروجی لانگ
public static long return_n_inputted(){
//ساخت شی اسکنر به همراه ورودی به کانستراکتور توسط سیستم این    
Scanner my_scanner = new Scanner(System.in) ;
//دریافت ورودی از کاربر    
long n = my_scanner.nextLong();
// ارسال به خروجی فانکشن
return n ;
}

}







