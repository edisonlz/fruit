package com.youku.api.gamestatis.adapter;

import java.util.ArrayList;
import java.util.HashMap;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.components.YAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.jjoe64.graphview.GraphView;
import com.youku.api.gamestatis.R;
import com.youku.api.gamestatis.adapter.HomeIndexAdapter.ViewHolder;

public class ShowRankAdapter extends BaseAdapter {

	private final ArrayList<HashMap<String,Object>> dataList;
	
	private final Context mContext;
	
	private boolean has_drawn = false;
	
	public ShowRankAdapter(Context context, ArrayList<HashMap<String,Object>> dataList) {
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
		
		
		if (null == convertView) {
			convertView = LayoutInflater.from(mContext).inflate(R.layout.showrank_item, parent, false);
        }
	
        
        HashMap<String,Object> data =(HashMap<String,Object>) this.dataList.get(position);
        
        TextView textViewName = (TextView)convertView.findViewById(R.id.textShowRankName);
        TextView textViewRate  = (TextView)convertView.findViewById(R.id.textShowRankRate);
        TextView textViewChannel = (TextView)convertView.findViewById(R.id.textShowRankChannel);
        TextView textViewVV = (TextView)convertView.findViewById(R.id.textShowRankVV);
        
        int playtimes = Integer.valueOf((String)data.get("playtimes"));
        int lasplaytimes = Integer.valueOf((String)data.get("lasplaytimes"));
        textViewName.setText(String.valueOf(data.get("showname")));
        textViewRate.setText(String.format("%.2f%%",(playtimes - lasplaytimes )*1.0/lasplaytimes * 100));
        textViewChannel.setText(String.valueOf(data.get("channel")));
        textViewVV.setText(String.format("%.2f万",playtimes * 1.0/10000));
       
        return convertView;
    }
	


}