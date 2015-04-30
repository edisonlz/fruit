package com.youku.api.gamestatis.adapter;

import android.content.Context;
import android.graphics.Color;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.EditText;
import java.util.ArrayList;
import java.util.HashMap;

import org.json.JSONArray;
import org.json.JSONException;


import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.Legend;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.components.YAxis.AxisDependency;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.utils.ColorTemplate;
import com.jjoe64.graphview.GraphView;

//import com.jjoe64.graphview.GraphView.GraphViewData;
import com.jjoe64.graphview.helper.StaticLabelsFormatter;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;
import com.youku.api.gamestatis.*;
import com.youku.api.gamestatis.util.UnitFormat;

public class HomeIndexAdapter extends BaseAdapter {

	private final ArrayList<HashMap<String,Object>> dataList;
	
	private final Context mContext;
	
	private boolean has_drawn = false;
	
	public HomeIndexAdapter(Context context, ArrayList<HashMap<String,Object>> dataList) {
		this.dataList = dataList;
		mContext = context;
    }
	
	@Override
	public int getCount() {
		return null != dataList ? dataList.size() : 0;
	}
	
	@Override
	public HashMap<String,Object> getItem(int position) {
	    return dataList.get(position);
	}
	
	@Override
	public long getItemId(int position) {
	    return position;
	}
	
	public String fixedLenString(String str,int length){
		int leave = length - str.length();
		
		if(leave>0){
			for(int i=0;i<leave;i++){
				str +=  " ";
			}
			
		}
		return str;
	}
	
	@Override
    public View getView(int position, View convertView, ViewGroup parent) {
		
		ViewHolder holder;
		if (null == convertView) {
			convertView = LayoutInflater.from(mContext).inflate(R.layout.home_table_list_item, parent, false);
        }
	
        
        HashMap<String,Object> data =(HashMap<String,Object>) this.dataList.get(position);
        
        
        TextView textViewName = (TextView)convertView.findViewById(R.id.textName);
        TextView textViewUV = (TextView)convertView.findViewById(R.id.textUV);
        TextView textViewVV = (TextView)convertView.findViewById(R.id.textVV);
        TextView textViewUVVV = (TextView)convertView.findViewById(R.id.textUVVV);
        
        textViewName.setText(fixedLenString((String)data.get("name"),5));
        textViewUV.setText(fixedLenString(String.valueOf(data.get("uv")),5));
        textViewVV.setText(fixedLenString(String.valueOf(data.get("vv")),5));
        textViewUVVV.setText(String.valueOf(data.get("uvvv")));
        
       
        /* Charts */
		
		//Log.e("error positoin graphview", String.valueOf(position));
        
        LineChart graphLayout_uv = (LineChart) convertView.findViewById(R.id.graphViewUV);
		
		HashMap<String,Object> uv_line = (HashMap<String,Object>) data.get("uv_line");
		drawGraphView(graphLayout_uv , uv_line);
		
		
		
		LineChart graphLayout_vv = (LineChart) convertView.findViewById(R.id.graphViewVV);
		HashMap<String,Object> vv_line = (HashMap<String,Object>) data.get("vv_line");
		
		drawGraphView(graphLayout_vv , vv_line);
		
		LineChart graphLayout_uvvv = (LineChart) convertView.findViewById(R.id.graphViewUVVV);
		HashMap<String,Object> uvvv_line = (HashMap<String,Object>) data.get("uvvv_line");
		
		drawGraphView(graphLayout_uvvv , uvvv_line);
		
        return convertView;
    }
	
	private void drawGraphView(LineChart graphView, HashMap<String,Object>  uv_line) {
		
		
		ArrayList<Integer> x = (ArrayList<Integer>)uv_line.get("x");
		ArrayList<Integer> y = (ArrayList<Integer>)uv_line.get("y");
		
		int num = x.size();
		
		if(num<=0){
			return;
		}
		
		Integer[] dates = new Integer[num];
		
		ArrayList<Entry> line1 = new ArrayList<Entry>();
		ArrayList<String> xVals = new ArrayList<String>();
	    
		int x_max = 0;
		int y_min = Integer.MAX_VALUE;
		int y_max = Integer.MIN_VALUE;
		for (int i = 0; i < num; i++) {
				dates[i] = x.get(i);
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
		
		y_min = y_min - (int)(y_min *0.1);
		y_max = y_max + (int)(y_max *0.1);
		
		//graphView.setBackgroundColor(Color.YELLOW);
		graphView.setTouchEnabled(false);
		graphView.setDragEnabled(false);
		graphView.setDrawBorders(false);
		graphView.setDrawGridBackground(false);
		graphView.setDrawMarkerViews(false);
		graphView.setGridBackgroundColor(Color.BLACK);
		graphView.setBorderColor(Color.BLACK);
		graphView.setBorderWidth(0);
		graphView.setDescription("");
		
		
		 
		YAxis yAxis = graphView.getAxisLeft();
		yAxis.setDrawLabels(false);
		yAxis.setDrawAxisLine(false);
		yAxis.setDrawGridLines(false);
		yAxis.setAxisLineWidth(0);
		yAxis.setLabelCount(2);
		
		//Log.e("y_max", String.valueOf(y_max));
		//Log.e("y_min", String.valueOf(y_min));
		yAxis.setStartAtZero(false);
		yAxis.setAxisMaxValue(y_max);
		yAxis.setAxisMinValue(y_min);
		yAxis.setShowOnlyMinMax(true);
		
		YAxis yrAxis = graphView.getAxisRight();
		yrAxis.setEnabled(false);

		
		XAxis xAxis = graphView.getXAxis();
		xAxis.setDrawLabels(false);
		xAxis.setDrawAxisLine(false);
		xAxis.setDrawGridLines(false);
		xAxis.setAxisLineWidth(0);
		
		LineDataSet setComp1 = new LineDataSet(line1, "");
		ArrayList<LineDataSet> dataSets = new ArrayList<LineDataSet>();
	    dataSets.add(setComp1);

	    setComp1.setDrawCircles(false); 
	    setComp1.setLineWidth(2f);
	    setComp1.setColor(Color.rgb(42, 136, 204));
	    
	    
	    LineData data = new LineData(xVals, dataSets);
	    data.setDrawValues(false);
	    graphView.setViewPortOffsets(4, 4, 0, 0);
	    graphView.setData(data);
	    graphView.getLegend().setEnabled(false);
	    
	    graphView.animateX(500);
	    
	}
	
	static class ViewHolder {
		
		TextView textViewName;
        TextView textViewUV;
        TextView textViewVV;
        TextView textViewUVVV;
        GraphView graphLayout_uv;
        GraphView graphLayout_vv;
        GraphView graphLayout_uvvv;
        
    }

}
