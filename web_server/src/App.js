import React from 'react';

import GraphSection from './components/GraphSection.js';
import scrollToComponent from 'react-scroll-to-component';
import IndexNavbar from './components/IndexNavbar'; 
import IndexHeader from './components/IndexHeader'; 
import MainBoard from './components/MainBoard';
import { ThemeProvider } from 'styled-components';

import theme from './styles/theme'; 
import './App.css';

export default class App extends React.Component {

	constructor(props) { 
		super(props); 
		this.mainBackground = { 
		}
	}
	
	render() { 
		return ( 
			<ThemeProvider theme={theme}>
				<IndexNavbar 
					toIndexHeader={() => scrollToComponent(this.IndexHeader, { offset: 0, align: 'top', duration: 1500, ease:'inExpo'})}
					toMainBoard={() => scrollToComponent(this.MainBoard, { offset: 0, align: 'top', duration: 1500})}
					toGraphSection={() => scrollToComponent(this.GraphSection, { offset: 0, align: 'top', duration: 1500})}
				/> 
				<IndexHeader ref={(IndexHeader) => { this.IndexHeader = IndexHeader;}} />
				<MainBoard  ref={(MainBoard) => { this.MainBoard = MainBoard; }} />
				<GraphSection 
					color='red' 
					ref={(GraphSection) => { this.GraphSection = GraphSection; }} />
				{/* <iframe src="http://localhost:5601/goto/d19e0bd25c1361ba71a02d38555f6e78" height="600" width="800"></iframe> */}
			</ThemeProvider>
		)
	}
}