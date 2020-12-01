import React from 'react';


import scrollToComponent from 'react-scroll-to-component';

import IndexNavbar from './components/IndexNavbar'; 
import IndexHeader from './components/indexHeader/IndexHeader'; 


import DomesticGraphSection from './components/domesticGraph/DomesticGraphSection'; 

import GlobalGraphSection from './components/globalGraph/GlobalGraphSection'; 
import PredGraphSection from './components/predGraph/PredGraphSection'; 


import NewsSection from './components/NewsInfo/NewsSections';
import InfoSection from './components/InfoSection'; 

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
					toIndexHeader={() => scrollToComponent(this.IndexHeader, 
											{ offset: 0, align: 'top', duration: 1500, ease:'inExpo'} )}
					toDomesticSection={() => scrollToComponent(this.DomesticDaily, 
											{ offset: 0, align: 'top', duration: 1500} )}

					toGlobalSection={() => scrollToComponent(this.GlobalGraphSection, 
											{ offset: 0, align: 'top', duration: 1500} )}
	
					toPredGraphSection={() => scrollToComponent(this.PredGraphSection, 
											{ offset: 0, align: 'top', duration: 1500} )}

					toNewsSection={() => scrollToComponent(this.NewsSection, 
											{ offset: 0, align: 'top', duration: 1500} )}
					toInfoSection={() => scrollToComponent(this.InfoSection, 
											{ offset: 0, align: 'top', duration: 1500} )}
				/> 

				<IndexHeader ref={(IndexHeader) => { this.IndexHeader = IndexHeader; }} />

				<DomesticGraphSection ref={(DomesticGraphSection) => { this.DomesticGraphSection = DomesticGraphSection; }} />

				<GlobalGraphSection ref={(GlobalGraphSection) => { this.GlobalGraphSection = GlobalGraphSection; }} />

				<PredGraphSection ref={(PredGraphSection) => { this.PredGraphSection = PredGraphSection; }} />

				<NewsSection ref={(NewsSection) => { this.NewsSection = NewsSection; }} />
				<InfoSection ref={(InfoSection) => { this.InfoSection = InfoSection; }} /> 

			</ThemeProvider>




		)
	}
}