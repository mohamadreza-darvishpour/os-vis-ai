// فراخوانی تابع اسکنر برای دریافت ورودی
import java.util.Scanner;

// ساخت کلاس ااصلی برنامه همنام با فایل
public class days_between{

//تابع اصلی برنامه برای اجرا 
public static void main(String[] args){

//حلقه بینهایت برای امتحان ورودی های مختلف
while(true){
// دستورات درون ترای انجام میشود در صورت ارور دستورات کچ
try{
//نمایش پیغام مناسب به کاربر برای دریافت ورودی
System.out.print("input dates : ");
// دریافت یک رشته شامل هر دو تاریخ با تابع نوشته شده در پایین
String date_string = ret_2_dates_str();
//محاسبه ی روز های *******دقیقا***** بین دو تاریخ یعنی خود روز ها محاسبه نمیشود
int diff_days = ret_diff_2_date_str(date_string);
// نمایش خروجی 
System.out.println("output : " + diff_days +" days");
// در صورت ارور در بخش ترای دستورات درون کچ انجام میشوند.
}catch(Exception e){
//نمایش پیغام مناسب
System.out.println("wrong inputted dates. try again.");
}
}


}


// فانکشن برای گرفتن استرینگ شامل هر دو تاریخ و ارسال تعداد روز های بین
public static int ret_diff_2_date_str(String two_dates){
// حذف فضای خالی درون استرینگ
String cleaned = two_dates.replace(" " , "");
// شکستن رشته ی شامل هر دو تاریخ به لیست دو رشته ی دو تاریخ
String[] dates_list  = cleaned.split(",");
// محاسبه ی تفاوت تعداد روزها از تاریخ 0/0/0 تا با تابع نوشته شده
int diff = ret_days_from_0_0_0(dates_list[0]) - ret_days_from_0_0_0(dates_list[1]);
//در صورت جابجایی تاریخ بزرگتر و کوچکتر مثبت کردن عدد حاصل
if(diff<0){
// ضرب عدد منفی در منفی برای مثب شدن نتیجه
diff = -1*diff;
}
//ارسال به خروجی
return diff;
}


//گرفتن رشته ی یک تاریخ به صورت 2/3/4 و محاسبه تعداد روز از تاریخ 0/0/0 و خروجی اینتجر
// سال های کبیثه و 31 روز بودن 6 ماه اول محاسبه شده.
public static int ret_days_from_0_0_0(String date_string){
//حذف کردن فضاهای خالی 
String dates_str = date_string.replace(" " ,"");
// شکستن تاریخ به روز و ماه و سال 
String date_list[] = dates_str.split("/");
// ذخیره و تبدیل رشته های روز ماه سال به عدد اینتجر
int day = Integer.parseInt(date_list[2]); 
int month = Integer.parseInt(date_list[1]);
int year = Integer.parseInt(date_list[0]);
// مجموع به صورتی که هر سال 365 و هر ماه 31 روز به همراه تعدادد روز همان تاریخ 
int sum = day + (month-1)*30 + year*365   ;  // need to delete additional days
//جمع با سال های کبیثه که یک روز اضاف دارد و هر 4 سال یک بار است.
sum = sum + (int)(year/4) ;  //any 4 years have 1 day more 
// سی و یک روزه بودن 6 ماه اول
if(  0 < month && month < 7){
sum = sum + (month -1);
}else{
sum = sum + 6;
}

//ارسال به خروجی
return sum ; 

}


// یک تابع برای گرفتن رشته ی حاوی دوتاریخ از کاربر
public static String ret_2_dates_str(){
//ساخت شی اسکنر با کانستراکتور سیستم این 
Scanner date_scanner = new Scanner(System.in);
//ذخیره ی ورودی در یک رشته با فراخوانی تابع نکست لاین از شی ساخته شده.
String date_str = date_scanner.nextLine();
//ارسال به خروجی به صورت رشته
return date_str;

}



}




















