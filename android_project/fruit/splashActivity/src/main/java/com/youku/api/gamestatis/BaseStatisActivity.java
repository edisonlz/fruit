package com.youku.api.gamestatis;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;

import org.json.JSONException;
import org.json.JSONObject;


import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.utils.ColorTemplate;
import com.github.mikephil.charting.utils.ValueFormatter;

import com.youku.api.gamestatis.adapter.ChartDataAdapter;
import com.youku.api.gamestatis.base.BaseActivity;
import com.youku.api.gamestatis.listviewitem.BarChartItem;
import com.youku.api.gamestatis.listviewitem.ChartItem;
import com.youku.api.gamestatis.listviewitem.LineChartItem;
import com.youku.api.gamestatis.listviewitem.ListDataCollection;
import com.youku.api.gamestatis.listviewitem.PieChartItem;
import com.youku.api.gamestatis.model.BaseStatisModel;
import com.youku.api.gamestatis.model.HttpCallBackHandler;
import com.youku.api.gamestatis.model.LoginModel;

import de.keyboardsurfer.android.widget.crouton.Crouton;
import de.keyboardsurfer.android.widget.crouton.Style;

import android.app.DatePickerDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;

import android.text.Editable;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

public class BaseStatisActivity   extends BaseActivity  {

	protected ProgressBar mProgressBar;
	private Context mContext;
	private Spinner platformSpinner;
	private Spinner deivceSpinner;
    private ArrayAdapter<String> platformAdapter;
    private ArrayAdapter<String> diviceAdapter;
    private Button  doButton; 
    private EditText startdateText;
    private EditText enddateText;
    Calendar myCalendar = Calendar.getInstance();

    
    private DatePickerDialog.OnDateSetListener sdatePickerListener 
				    = new DatePickerDialog.OnDateSetListener() {
			public void onDateSet(DatePicker view, int selectedYear,
				int selectedMonth, int selectedDay) {
				
				startdateText.setText(String.format("%d%02d%02d", selectedYear,selectedMonth+1,selectedDay));
			}
    };
    
    private DatePickerDialog.OnDateSetListener edatePickerListener 
	    = new DatePickerDialog.OnDateSetListener() {
		public void onDateSet(DatePicker view, int selectedYear,
		int selectedMonth, int selectedDay) {
			enddateText.setText(String.format("%d%02d%02d", selectedYear,selectedMonth+1,selectedDay));
		}
		
	};
	
	public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        
        mContext = this;
        
        setContentView(R.layout.basestatis);
        
        setUpViews();
        String item_id = this.getProduct();
		if (item_id == null) {
			Toast.makeText(this, String.valueOf("请选择产品线!"),
					Toast.LENGTH_SHORT).show();
			return;
		}

		loadData();
	}
	
	private void setUpViews() {
		mProgressBar = (ProgressBar) this.findViewById(R.id.ajax_loading);
		mProgressBar.setVisibility(View.VISIBLE);
		
		platformSpinner = (Spinner) findViewById(R.id.platformSpinner);
        
        deivceSpinner = (Spinner) findViewById(R.id.deivceSpinner);
        
        doButton = (Button)findViewById(R.id.doButton);
        
        doButton.setOnClickListener(new View.OnClickListener(){

			@Override
			public void onClick(View v) {
				loadData();
			}});
        
        startdateText = (EditText) findViewById(R.id.startdateText);
        
        startdateText.setFocusable(false);
        
        startdateText.setOnClickListener(new View.OnClickListener() {
 
			@Override
			public void onClick(View v) {

				Editable date = startdateText.getText();
				
				int year = Integer.valueOf(date.toString().substring(0,4));
				int month = Integer.valueOf(date.toString().substring(4,6))-1;
				int day = Integer.valueOf(date.toString().substring(6,8));
				

				new DatePickerDialog(BaseStatisActivity.this, sdatePickerListener, year,month,day).show();
			}
 
		});
        
        enddateText = (EditText) findViewById(R.id.enddateText);
        enddateText.setFocusable(false);
        enddateText.setOnClickListener(new View.OnClickListener() {
 
			@Override
			public void onClick(View v) {
				Editable date = enddateText.getText();
				int year = Integer.valueOf(date.toString().substring(0,4));
				int month = Integer.valueOf(date.toString().substring(4,6))-1;
				int day = Integer.valueOf(date.toString().substring(6,8));
				
				new DatePickerDialog(BaseStatisActivity.this, edatePickerListener, year,month,day).show();
			}
 
		});
        
	}

	
	private void loadData(){
		
		mProgressBar.setVisibility(View.VISIBLE);
		
		String splatform = platformSpinner.getSelectedItem().toString();
		String sdevice = deivceSpinner.getSelectedItem().toString();
		
        
		int device = this.deivceMap.get(sdevice);
		int platform = this.platformMap.get(splatform);
        
		BaseStatisModel commonStats = new BaseStatisModel(this);
		commonStats.get(this.getProduct(),platform,device,new HttpCallBackHandler() {

			@Override
			public void onSuccess(HashMap<String, Object> result) {
				onHttpResponseCallback(result);
				mProgressBar.setVisibility(View.INVISIBLE);
			}

			@Override
			public void onFailure(Throwable error, String content) {
				mProgressBar.setVisibility(View.INVISIBLE);
				if (error != null) {
					Crouton.makeText(BaseStatisActivity.this,   error.getMessage(), Style.CONFIRM).show();
				}
				if (content != null) {
					Crouton.makeText(BaseStatisActivity.this, content.toString(), Style.CONFIRM).show();
				}
			}

			@Override
			public void onFailure(Throwable error, JSONObject obj) {
				mProgressBar.setVisibility(View.INVISIBLE);
				if (error != null) {
					String msg = error.getMessage();
					if(msg==null){
						msg = "读取接口错误";
					}
					Crouton.makeText(BaseStatisActivity.this,  msg, Style.CONFIRM).show();
				}
				if (obj != null) {
					Crouton.makeText(BaseStatisActivity.this, obj.toString(), Style.CONFIRM).show();
				}
			}

		});
	}

	public void onHttpResponseCallback(HashMap<String, Object> result) {

		/* Set List View */
		
		HashMap<String,Object> data = (HashMap<String,Object>)result.get("data");
		EditText startdateText =  (EditText)this.findViewById(R.id.startdateText);
		EditText enddateText =   (EditText)this.findViewById(R.id.enddateText);
		TextView productText = (TextView)this.findViewById(R.id.productText);
		
		startdateText.setText(String.valueOf(result.get("startdate")));
		enddateText.setText(String.valueOf(result.get("enddate")));
		productText.setText(String.valueOf(result.get("product_name")));
		
		String enddate = String.valueOf(result.get("enddate"));
		
		ArrayList<ChartItem> list = new ArrayList<ChartItem>();
		ListView chartListView = (ListView)this.findViewById(R.id.chartlistView);
        
		HashMap<String,Object>  uv_line =  (HashMap<String,Object>)data.get("uv_line");
		
		
		ListDataCollection ldc = generateDataLine(uv_line,Color.rgb(70, 198,226),10000);
		list.add(new LineChartItem(ldc.dataSet, getApplicationContext(),10000,"W",ldc.yMax,ldc.yMin,ldc.is_viewport));
		
		HashMap<String,Object>  vv_line =  (HashMap<String,Object>)data.get("vv_line");
		ListDataCollection ldc2 = generateDataLine(vv_line,Color.rgb(247,80,90),10000);
		list.add(new LineChartItem(ldc2.dataSet, getApplicationContext(),10000,"W",ldc2.yMax,ldc2.yMin,ldc2.is_viewport));
		
		ArrayList uv_rate =  (ArrayList)data.get("uv_rate");
		list.add(new PieChartItem(generateDataPie(uv_rate), getApplicationContext(),String.format("%s\n%s","UV分布",enddate)));

		ChartDataAdapter cda = new ChartDataAdapter(getApplicationContext(), list);
		chartListView.setAdapter(cda);
	}
	
	
	private PieData generateDataPie(ArrayList uv_rate) {

        ArrayList<Entry> entries = new ArrayList<Entry>();
        ArrayList<String> q = new ArrayList<String>();
        
        for (int i = 0; i < uv_rate.size(); i++) {
        	HashMap<String,Integer> map = (HashMap<String,Integer>) uv_rate.get(i);
        	
        		for(String key: map.keySet()){  
        			entries.add(new Entry(map.get(key), i));
        			q.add(key);
        		}
        }

        PieDataSet d = new PieDataSet(entries, "");
        
        // space between slices
        d.setSliceSpace(2f);
        d.setColors(ColorTemplate.VORDIPLOM_COLORS);
        
        PieData cd = new PieData(q, d);
        return cd;
    }
	
	
	
	 private ListDataCollection generateDataLine(HashMap<String,Object>  uv_line,int color,int divide) {

		 	ArrayList<Integer> x = (ArrayList<Integer>)uv_line.get("x");
			ArrayList<Integer> y = (ArrayList<Integer>)uv_line.get("y");
			
			int num = x.size();
			
		 
			ArrayList<Entry> line1 = new ArrayList<Entry>();
			ArrayList<String> xVals = new ArrayList<String>();
		    
			int x_max = 0;
			int y_min = Integer.MAX_VALUE;
			int y_max = Integer.MIN_VALUE;
			for (int i = 0; i < num; i++) {
					x_max = i;
					if(y.get(i)>y_max){
						y_max = y.get(i);
					}
					if(y.get(i)<y_min){
						y_min = y.get(i);
					}
					
					Entry entry = new Entry(y.get(i), i); 
				    line1.add(entry);
				    xVals.add(String.valueOf(x.get(i)));
			}


	        LineDataSet d1 = new LineDataSet(line1, (String)uv_line.get("name"));
	        d1.setLineWidth(2.5f);
	        d1.setCircleSize(3f);
	        //d1.setDrawCircles(false);
	        d1.setHighLightColor(Color.rgb(244, 117, 117));
	        d1.setCircleColor(color);
	        d1.setFillColor(color);
	        d1.setDrawValues(true);
	        d1.setValueFormatter(new MyValueFormatter(divide));
	        d1.setDrawCubic(true);
		    d1.setCubicIntensity(0.2f);
		    d1.setDrawFilled(true);
		    d1.setColor(color);
		    
	        
	        ArrayList<LineDataSet> sets = new ArrayList<LineDataSet>();
	        sets.add(d1);
	        
	        LineData cd = new LineData(xVals, sets);
	        
	        ListDataCollection ldc = new ListDataCollection(cd,y_max,y_min);
	        return ldc;
	    }
	 	
	 
	 	private static class MyValueFormatter implements ValueFormatter {

	        private int divide;

	        public MyValueFormatter(int divide) {
	            this.divide = divide;
	        }

	        @Override
	        public String getFormattedValue(float value) {
	        	return String.format("%s",Integer.valueOf( (int) (value/divide)));
	        }
	    }
	 	
	 	@Override
	    public void onDestroy(){
	    	super.onDestroy();
	    	Crouton.cancelAllCroutons();
	    }
}