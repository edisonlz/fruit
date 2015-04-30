package com.youku.api.gamestatis.listviewitem;

import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;

public class ListDataCollection {
	
	
	public LineData dataSet;
	
	public int yMax;
	
	public int yMin;
	
	public boolean is_viewport = true;
	
	public ListDataCollection(LineData dataSet,int yMax,int yMin){
		this.dataSet = dataSet;
		this.yMax = yMax;
		this.yMin = yMin;
	}
	
	public ListDataCollection(LineData dataSet){
		this(dataSet,0,0);
		this.enableViewPort(false);
	}
	
	
	public void enableViewPort(boolean en){
		this.is_viewport = en;
	}

}
