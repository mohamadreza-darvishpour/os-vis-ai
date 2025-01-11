
import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;


public class list_avg{

public static void main(String[] args){
    
    while(true){
    try{
    // 3,34,9
    System.out.print( "Enter your numbers : "   );
    String num_text = return_inputted_string();
    String[] num_list = num_text.split(",");
    List<Double> mix_list = new ArrayList<>() ;
    for (String item : num_list ){
        double changed_type = Double.parseDouble(item);
        mix_list.add(changed_type);
    }
    double avg = return_avg_from_list(mix_list);
    System.out.println("List : " + mix_list);
    System.out.println("Avg = " + avg);
    }
    catch(Exception e ){
        System.out.println("wrong input amount. try again.");
    }
    }
}


public static String return_inputted_string(){
    Scanner my_scanner = new Scanner(System.in);
    String text = my_scanner.nextLine();
    return text ;
}

public static double return_avg_from_list(List<Double> any_list){
    double sum = 0;
    for(double item : any_list){
    sum = sum + item ;
}   
    return (sum/ any_list.size()   ) ;

}

}








