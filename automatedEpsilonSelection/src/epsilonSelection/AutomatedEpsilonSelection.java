package epsilonSelection;

import java.io.FileReader;
import java.util.*;
import java.util.stream.Collectors;

import com.opencsv.CSVReader;

public class AutomatedEpsilonSelection {

	public AutomatedEpsilonSelection() {
		// TODO Auto-generated constructor stub
	}
	
	@SuppressWarnings("resource")
	public static void main(String[] args) throws Exception {
//		Read an input csv file. Place the file in the project directory.
//		Build reader instance
		CSVReader reader = new CSVReader(new FileReader("dataSet.csv"), ',', '"', 0);
//		Read all rows at once
		List<String[]> allRows = reader.readAll();
		long order = 0;
//		Take one vector at a time and find its k-nearest neighbors.
		for(String[] arrayRow : allRows) {
			order = order + 1;
			String stringOrder = String.valueOf(order);
			List<String> arrayListRow = new ArrayList<String>(Arrays.asList(arrayRow));
			arrayListRow.add(stringOrder);
			List<Double> row = arrayListRow.stream().map(Double::valueOf).collect(Collectors.toList());
			System.out.println(row);
		}
			
//	        System.out.println(Arrays.toString(row));
		

	}

}
