package epsilonSelection;

import java.io.FileReader;
import java.util.*;

import com.opencsv.CSVReader;

public class AutomatedEpsilonSelection {

	public AutomatedEpsilonSelection() {
		// TODO Auto-generated constructor stub
	}
	
	@SuppressWarnings("resource")
	public static void main(String[] args) throws Exception {
//		Read an input csv file. Place the file in the project directory.
//		Build reader instance
		CSVReader reader = new CSVReader(new FileReader("dataSet.csv"), ',', '"', 1);
//		Read all rows at once
		List<String[]> allRows = reader.readAll();
//		Append an order = 0 to each row.
		for(String[] row : allRows) {
			List<String> rowAsArrayList = new ArrayList<String>(Arrays.asList(row));
			rowAsArrayList.add("0");
			System.out.println(rowAsArrayList);
		}
			
//	        System.out.println(Arrays.toString(row));
		

	}

}
